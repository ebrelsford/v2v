from django.utils.translation import ugettext_lazy as _

from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
import feincms_cleanse

from elephantblog.models import Entry


Entry.register_extensions(
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',
)

Entry.register_regions(
    ('main', _('Main content area')),
)

Entry.create_content_type(RichTextContent,
                          cleanse=feincms_cleanse.cleanse_html,
                          regions=('main',)
)

Entry.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
