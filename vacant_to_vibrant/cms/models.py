from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent

from pathways.models import Pathway


class PathwayListContent(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('pathway list')
        verbose_name_plural = _('pathway lists')

    def render(self, **kwargs):
        context = {
            'pathway_list': Pathway.objects.all().order_by('name'),
        }
        context.update(kwargs)
        return render_to_string([
            'pathways/page_content_list.html',
        ], context, context_instance=kwargs.get('context'))


class CollapsibleSectionContent(RichTextContent):

    title = models.CharField(_('title'), max_length=200)
    start_collapsed = models.BooleanField(_('start collapsed'), default=False)

    class Meta:
        abstract = True
        verbose_name = _('collapsible section')
        verbose_name_plural = _('collapsible sections')

    def render(self, **kwargs):
        return render_to_string('cms/collapsiblesection/default.html',
            { 'content': self }, context_instance=kwargs.get('context'))


class RecentActivitiesContent(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('recent activity list')
        verbose_name_plural = _('recent activity lists')

    def render(self, **kwargs):
        return render_to_string([
            'activity/plugin.html',
        ], {}, context_instance=kwargs.get('context'))


Page.register_extensions(
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations'
)

Page.register_templates({
    'title': _('Standard template'),
    'path': 'base.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ('footer', _('Footer'), 'inherited'),
    ),
})

Page.register_templates({
    'title': _('Home map template'),
    'path': 'home_map.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ('footer', _('Footer'), 'inherited'),
    ),
})

Page.create_content_type(RichTextContent)

Page.create_content_type(CollapsibleSectionContent)
Page.create_content_type(PathwayListContent)
Page.create_content_type(RecentActivitiesContent)

Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('lots.map_urls', _('Lots map')),
    ('elephantblog.urls', _('Blog')),
    ('extraadmin.cms_urls', _('Extra admin functions')),
    ('pathways.urls', _('Pathways')),
    ('contact_form', _('Contact form'), {
        'urls': 'contact.form_urls',
    }),
    ('contact_success', _('Contact success'), {
        'urls': 'contact.success_urls',
    }),
))


Pathway.register_extensions(
    'feincms.module.extensions.translations',
)

Pathway.register_regions(
    ('main', _('Main content area')),
)

Pathway.create_content_type(RichTextContent)

Pathway.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
