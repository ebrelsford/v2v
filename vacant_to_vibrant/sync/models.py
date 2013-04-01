from django.db import models
from django.utils.translation import ugettext_lazy as _

from .synchronizers import do_synchronize


class DataSource(models.Model):
    """
    An external data source that is periodically updated. Will not be updated
    unless a Synchronizer is defined that will do the updating.

    """

    #
    # TODO consider https://bitbucket.org/wnielson/django-chronograph/src
    #  for syncing.
    #
    # OR
    #  http://docs.celeryproject.org/en/master/getting-started/introduction.html
    # (via)
    #  http://chase-seibert.github.com/blog/2010/07/09/djangocelery-quickstart-or-how-i-learned-to-stop-using-cron-and-love-celery.html
    #

    description = models.TextField(_('description'),
        blank=True,
        null=True,
    )

    enabled = models.BooleanField(_('enabled'),
        default=True,
    )

    healthy = models.BooleanField(_('healthy'),
        default=True,
        help_text=_('Was synchronizing successful last attempt?'),
    )

    ordering = models.IntegerField(_('ordering'),
        default=1,
        help_text=_('The ordering of this source, lower numbers coming first.'),
    )

    synchronize_frequency = models.IntegerField(_('synchronize frequency'),
        blank=True,
        null=True,
        help_text=_('The number of hours that should pass between '
                    'synchronizations of this source.'),
    )

    next_synchronize = models.DateTimeField(_('next synchronize'),
        blank=True,
        null=True,
        help_text=_('The next time this data source should be synchronized.'),
    )

    last_synchronized = models.DateTimeField(_('last synchronized'),
        help_text=_('The last time this data source was synchronized'),
    )

    def synchronize(self):
        do_synchronize(self)

    def __unicode__(self):
        return u'%s' % (self.name,)

    class Meta:
        abstract = True
        ordering = ('ordering',)
