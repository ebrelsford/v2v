from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class ContentForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(
        label='content type',
        queryset=ContentType.objects.all(),
        widget=forms.HiddenInput()
    )

    object_id = forms.IntegerField(
        label='object id',
        widget=forms.HiddenInput()
    )

    added_by = forms.ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        required=False,
        widget=forms.HiddenInput()
    )

    added_by_name = forms.CharField(
        label=_('Your name'),
        max_length=256,
        required=False,
        widget=forms.TextInput(),
    )

    def __init__(self, *args, **kwargs):
        # add initial value for added_by based on the user kwarg
        kwargs['initial'] = kwargs.get('initial', {})
        user = kwargs.get('user', None)
        if not user or user.is_anonymous(): user = None
        kwargs['initial']['added_by'] = user

        super(ContentForm, self).__init__(*args, **kwargs)
