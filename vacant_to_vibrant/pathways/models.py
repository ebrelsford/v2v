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

        # Ownership filters
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

        # L&I filters
        licenses_exist = lot.licenses.count() != 0
        pathways = pathways.filter(Q(has_licenses=licenses_exist) |
                                   Q(has_licenses=None))
        violations_exist = lot.violations.count() != 0
        pathways = pathways.filter(Q(has_violations=violations_exist) |
                                   Q(has_violations=None))

        # Available property filters
        is_available_property = lot.available_property is not None
        pathways = pathways.filter(Q(is_available_property=is_available_property) |
                                   Q(is_available_property=None))
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
    is_available_property = models.NullBooleanField(_('is available property'),
        help_text=_("Is the lot in the PRA's available property list?"),
    )
    has_licenses = models.NullBooleanField(_('has licenses from L&I'),
        help_text=_('Does the lot have vacancy-related licenses from L&I?'),
    )
    has_violations = models.NullBooleanField(_('has violations from L&I'),
        help_text=_('Does the lot have vacancy-related violations from L&I?'),
    )

    def __unicode__(self):
        return self.name

    @app_models.permalink
    def get_absolute_url(self):
        return ('pathway_detail', 'pathways.urls', (), {
            'slug': self.slug,
        })
