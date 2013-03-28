import copy

from django import forms
from django.contrib import messages
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.generic import FormView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from lots.models import Lot
from .models import Alias, Owner

class AddAnotherWidgetWrapper(forms.Widget):
    """
    This class is a wrapper to a given widget to add the add icon for the
    admin interface.
    """
    def __init__(self, widget, model):
        self.is_hidden = widget.is_hidden
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.widget = widget
        self.model = model

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.widget = copy.deepcopy(self.widget, memo)
        obj.attrs = self.widget.attrs
        memo[id(self)] = obj
        return obj

    @property
    def media(self):
        return self.widget.media

    def render(self, name, value, *args, **kwargs):
        model = self.model
        info = (model._meta.app_label, model._meta.object_name.lower())
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        related_url = reverse('admin:%s_%s_add' % info)
        output.append(('<a href="%s" class="add-another" id="add_id_%s" ' +
                      'onclick="return showAddAnotherPopup(this);"> ')
                      % (related_url, name))
        output.append('<img src="%s" width="10" height="10" alt="%s"/></a>'
                      % (static('admin/img/icon_addlink.gif'),
                         _('Add Another')))
        return mark_safe(''.join(output))

    def build_attrs(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        self.attrs = self.widget.build_attrs(extra_attrs=None, **kwargs)
        return self.attrs

    def value_from_datadict(self, data, files, name):
        return self.widget.value_from_datadict(data, files, name)

    def _has_changed(self, initial, data):
        return self.widget._has_changed(initial, data)

    def id_for_label(self, id_):
        return self.widget.id_for_label(id_)


class MakeAliasesForm(forms.Form):
    owner = forms.ModelChoiceField(
        queryset=Owner.objects.all().order_by('name'),
        widget=AddAnotherWidgetWrapper(
            forms.Select(),
            Owner,
        )
    )

    owners_to_delete = forms.ModelMultipleChoiceField(
        queryset=Owner.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )


class MakeAliasesView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = MakeAliasesForm
    permission_required = ('owners.add_owner', 'owners.delete_alias',)
    template_name = 'admin/owners/owner/make_aliases.html'

    def get_context_data(self, **kwargs):
        context = super(MakeAliasesView, self).get_context_data(**kwargs)
        context.update({
            'is_popup': False,
            'opts': Owner._meta,
            'title': _('Make Aliases'),
            'owners_to_delete': Owner.objects.filter(
                pk__in=self.request.GET.get('ids', '').split(','),
            ).order_by('name'),
        })
        return context

    def get_initial(self):
        initial = super(MakeAliasesView, self).get_initial()
        initial.update({
            'owners_to_delete': Owner.objects.filter(
                pk__in=self.request.GET.get('ids', '').split(','),
            ),
        })
        return initial

    def get_success_url(self):
        return reverse('admin:owners_owner_changelist')

    def form_valid(self, form):
        owner = form.cleaned_data['owner']
        owners_to_delete = form.cleaned_data['owners_to_delete']
        aliases_added = owners_to_delete.count()

        self._add_aliases(owner, owners_to_delete)
        self._delete_aliased_owners(owner, owners_to_delete)

        messages.success(self.request,
                         'Added %d aliases to %s' % (aliases_added, owner.name))
        return super(MakeAliasesView, self).form_valid(form)

    def _add_aliases(self, owner, owners_to_delete):
        """Add aliases to the given owner."""
        for owner_to_delete in owners_to_delete:
            alias, created = Alias.objects.get_or_create(
                name=owner_to_delete.name
            )
            owner.aliases.add(alias)
        owner.save()

    def _delete_aliased_owners(self, owner, owners_to_delete):
        """
        Delete owners that are now aliases, reassigning related models first.
        """
        for owner_to_delete in owners_to_delete:
            Lot.objects.filter(owner=owner_to_delete).update(owner=owner)
        owners_to_delete.delete()
