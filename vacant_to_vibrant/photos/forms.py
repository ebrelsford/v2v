from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.forms import HiddenInput, IntegerField, ModelChoiceField

from vacant_to_vibrant.forms import CaptchaForm
from .models import Photo


class PhotoForm(CaptchaForm):
    content_type = ModelChoiceField(
        label='content type',
        queryset=ContentType.objects.all(),
        widget=HiddenInput()
    )

    object_id = IntegerField(
        label='object id',
        widget=HiddenInput()
    )

    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        required=False,
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        # add initial value for added_by based on the user kwarg
        kwargs['initial'] = kwargs.get('initial', {})
        user = kwargs.get('user', None)
        if not user or user.is_anonymous(): user = None
        kwargs['initial']['added_by'] = user

        super(PhotoForm, self).__init__(*args, **kwargs)

    class Meta:
        exclude = ('added',)
        model = Photo
