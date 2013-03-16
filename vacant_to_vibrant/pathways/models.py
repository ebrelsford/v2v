from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.models import Base
from feincms.module.mixins import ContentModelMixin


class Pathway(ContentModelMixin, Base):
    name = models.CharField(_('name'), max_length=256, null=True, blank=True)
    slug = models.SlugField(_('slug'), max_length=256, null=True, blank=True)
    is_active = models.BooleanField(_('is active'), default=True, db_index=True)
    author = models.ForeignKey(User, verbose_name=_('author'))

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('pathway_detail', (), { 'slug': self.slug, })
