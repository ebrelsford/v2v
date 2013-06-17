from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

import django_monitor


class BaseStewardProject(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    use = models.ForeignKey('lots.Use',
        limit_choices_to={'visible': True},
        help_text=_('How is the project using the land?'),
        verbose_name=_('use'),
    )
    support_organization = models.CharField(_('support organization'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_("What is your project's support organization, if any?"),
    )
    land_tenure_status = models.CharField(_('land tenure status'),
        choices=(
            ('owned', _('project owns the land')),
            ('licensed', _('project has a license for the land')),
            ('lease', _('project has a lease for the land')),
            ('access', _('project has access to the land')),
            ('not sure', _("I'm not sure")),
        ),
        default=_('not sure'),
        max_length=50,
        help_text=_('What is the land tenure status for the project? (This '
                    'will not be shared publicly.)'),
    )
    include_on_map = models.BooleanField(_('include on map'),
        default=False,
        help_text=_('Can we include the project on our map?'),
    )

    class Meta:
        abstract = True


class StewardProject(BaseStewardProject):

    organizer = models.ForeignKey('phillyorganize.Organizer',
        verbose_name=_('organizer'),
        help_text=_('The organizer associated with this project.'),
    )

    def __unicode__(self):
        return self.organizer.name


class StewardNotification(BaseStewardProject):
    """
    A notification from someone who is part of a stewarding project letting us
    know that they are stewards on a given lot. Basically an Organizer and a
    StewardProject, combined here so they can be moderated simultaneously.

    """
    name = models.CharField(_('name'),
        max_length=256,
        help_text=_('The name of the project using this lot.'),
    )
    phone = models.CharField(_('phone'),
        max_length=32,
        null=True,
        blank=True,
        help_text=_('A phone number where the project can be reached.'),
    )
    email = models.EmailField(_('email'),
        help_text=_('An email address where the project can be reached.'),
    )
    type = models.ForeignKey('organize.OrganizerType',
        help_text=_('The type of group working on the project.'),
    )
    url = models.URLField(_('url'),
        null=True,
        blank=True,
        help_text=_('A website where others can learn more about the project.'),
    )
    facebook_page = models.CharField(
        _('facebook page'),
        max_length=256,
        null=True,
        blank=True,
        help_text=('The Facebook page for the project. Please do not enter '
                   'your personal Facebook page.'),
    )

    def __unicode__(self):
        return self.name


django_monitor.nq(StewardNotification)

# Disconnect monitor's post-save handler
from django.db.models.signals import post_save

from django_monitor.util import save_handler

post_save.disconnect(save_handler, sender=StewardNotification)


#
# Signals
#
from django.dispatch import receiver

from django_monitor import post_moderation


@receiver(post_moderation, sender=StewardNotification,
          dispatch_uid='steward_stewardnotification')
def create_steward_project_and_organizer(sender, instance, **kwargs):
    """
    Once a StewardNotification is moderated and approved, make it official by
    creating an Organizer object and StewardProject as defined by the
    StewardNotification.
    """
    if not instance.is_approved:
        return

    # Create an organizer
    from phillyorganize.models import Organizer

    organizer = Organizer(
        content_type=instance.content_type,
        object_id=instance.object_id,
        name=instance.name,
        phone=instance.phone,
        email=instance.email,
        type=instance.type,
        url=instance.url,
        facebook_page=instance.facebook_page,
    )
    organizer.save()

    # Create a steward project
    steward_project = StewardProject(
        organizer=organizer,
        content_type=instance.content_type,
        object_id=instance.object_id,
        use=instance.use,
        support_organization=instance.support_organization,
        land_tenure_status=instance.land_tenure_status,
    )
    steward_project.save()

    steward_project.content_object.known_use = steward_project.use
    steward_project.content_object.save()
