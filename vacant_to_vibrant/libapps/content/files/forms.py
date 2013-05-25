from ..forms import ContentForm
from .models import File


class FileForm(ContentForm):

    class Meta:
        fields = ('added_by_name', 'document', 'title', 'description',
                  'content_type', 'object_id',)
        model = File
