from django.db import models
from django.utils.translation import ugettext_lazy as _


class Owner(models.Model):

    name = models.CharField(_('name'),
        max_length=256,
        unique=True,
    )

    # TODO refer back to opa.AccountOwner
    # TODO owner_type
    # TODO aliases / LLCs ?
    # TODO agency code from PRA data

    def __unicode__(self):
        return u'%s' % (self.name,)

