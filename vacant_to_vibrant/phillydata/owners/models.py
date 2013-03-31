from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _

import reversion


class OwnerManager(models.Manager):

    def get_or_create(self, name, defaults={}):
        """Get or create an owner while taking aliases into account."""
        try:
            return self.get(name__iexact=name)
        except ObjectDoesNotExist:
            try:
                return self.get(aliases__name__iexact=name)
            except ObjectDoesNotExist:
                return self.create(name=name, **defaults)


class Alias(models.Model):
    name = models.CharField(_('name'),
        max_length=256,
        unique=True,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('alias')
        verbose_name_plural = _('aliases')


class Owner(models.Model):

    objects = OwnerManager()

    name = models.CharField(_('name'),
        max_length=256,
        unique=True,
    )

    OWNER_TYPE_CHOICES = (
        ('private', 'private'),
        ('public', 'public'),
        ('unknown', 'unknown'),
    )
    owner_type = models.CharField(_('owner type'),
        choices=OWNER_TYPE_CHOICES,
        default='unknown',
        max_length=20,
    )

    aliases = models.ManyToManyField('Alias',
        help_text=_('Other names for this owner'),
        verbose_name=_('aliases'),
        blank=True,
        null=True,
    )
    agency_codes = models.ManyToManyField('AgencyCode',
        help_text=_('Agency codes used to refer to this owner'),
        verbose_name=_('agency codes'),
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.owner_type)

    def add_alias(self, alias_name):
        alias, created = Alias.objects.get_or_create(name=alias_name)
        self.aliases.add(alias)
        return alias

    def make_alias(self, other_owner):
        """Make other_owner an alias for this owner."""

        # redirect all relationships to this owner
        for related in self._meta.get_all_related_objects():
            related.model.objects.filter(owner=other_owner).update(owner=self)

        # redirect aliases to this owner
        for alias in other_owner.aliases.all():
            self.aliases.add(alias)
        self.add_alias(other_owner.name)

        # get rid of the other owner
        other_owner.delete()


class AgencyCode(models.Model):
    """
    A code used in city data that refers to an agency as a property owner.

    """
    code = models.CharField(_('code'),
        max_length=256,
        unique=True,
    )

    def __unicode__(self):
        return self.code

reversion.register(Owner)
