from django.contrib import messages
from django.template import RequestContext
from django.views.generic import FormView

from forms_builder.forms import signals
from forms_builder.forms.models import Form

from .forms import SurveyFormForForm


class SurveyView(FormView):
    form_class = SurveyFormForForm

    def get_form(self, form_class):
        form = Form.objects.get(pk=self.kwargs['pk'])
        request_context = RequestContext(self.request)
        args = (form, request_context, self.request.POST or None,
                self.request.FILES or None)
        return form_class(*args)

    def form_invalid(self, form):
        signals.form_invalid.send(sender=self.request, form=form)
        return super(SurveyView, self).form_invalid(form)

    def form_valid(self, form):
        entry = form.save()
        self.content_object = entry.content_object
        messages.success(self.request, 'Successfully updated survey.')
        signals.form_valid.send(sender=self.request, form=form, entry=entry)
        return super(SurveyView, self).form_valid(form)

    def get_success_url(self):
        return self.content_object.get_absolute_url()
