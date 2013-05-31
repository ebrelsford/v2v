from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from feincms.content.application import models as app_models
from feincms.models import Base
from feincms.module.mixins import ContentModelMixin


class PathwayManager(models.Manager):

    def get_for_lot(self, lot):
        pathways = self.all()
        if not lot or not lot.owner:
            return self.none()
        if lot.owner.owner_type == 'private':
            pathways = pathways.filter(private_owners=True)
        elif lot.owner.owner_type == 'public':
            # Public lots: get pathways for public owners and pathways that
            # either do not specify certain public owners or match the given
            # lot's owner
            pathways = pathways.filter(
                (Q(specific_public_owners__isnull=True) |
                 Q(specific_public_owners=lot.owner)),
                public_owners=True
            )
        return pathways


class Pathway(ContentModelMixin, Base):
    objects = PathwayManager()

    name = models.CharField(_('name'), max_length=256)
    slug = models.SlugField(_('slug'), max_length=256)
    is_active = models.BooleanField(_('is active'), default=True,
                                    db_index=True)
    author = models.ForeignKey(User, verbose_name=_('author'), null=True,
                               blank=True)

    # Filters for determining which lots a pathway can apply to
    private_owners = models.BooleanField(_('private owners'),
        help_text=_('This pathway applies to lots with private owners.'),
    )
    public_owners = models.BooleanField(_('public owners'),
        help_text=_('This pathway applies to lots with public owners.'),
    )
    specific_public_owners = models.ManyToManyField('owners.Owner',
        blank=True,
        null=True,
        limit_choices_to={'owner_type': 'public',},
        help_text=_('This pathway applies to lots with the given  public '
                    'owners.'),
    )

    def __unicode__(self):
        return self.name

    @app_models.permalink
    def get_absolute_url(self):
        return ('pathway_detail', 'pathways.urls', (), {
            'slug': self.slug,
        })
