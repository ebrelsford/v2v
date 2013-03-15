from django.db import models
from django.utils.translation import ugettext_lazy as _


class Pathway(models.Model):
    name = models.CharField(_('name'), max_length=256, null=True, blank=True)
    slug = models.SlugField(_('slug'), max_length=256, null=True, blank=True)
