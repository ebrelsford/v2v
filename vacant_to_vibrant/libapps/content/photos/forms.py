from django import forms
from django.utils.translation import ugettext_lazy as _

from ..forms import ContentForm
from .models import Photo


class PhotoForm(ContentForm):

    original_image = forms.ImageField(
        label=_('Photo file'),
    )

    class Meta:
        fields = ('added_by_name', 'original_image', 'name', 'description',
                  'content_type', 'object_id',)
        model = Photo
