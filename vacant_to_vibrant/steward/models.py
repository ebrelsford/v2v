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
        help_text=_('How is the project using the land?'),
        verbose_name=_('use'),
    )
    part_of_nga = models.BooleanField(
        _('part of Neighborhood Garden Association'),
        default=False,
        help_text=_('Is your project part of the Neighborhood Garden '
                    'Association?'),
    )
    support_organization = models.CharField(_('support organization'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_("What is your project's support organization, if any?"),
    )
    farm_stand = models.BooleanField(_('farm stand'),
        default=False,
        help_text=_('Does your project have a farm stand?'),
    )
    waiting_list = models.BooleanField(_('waiting list'),
        default=False,
        help_text=_('Does your project have a waiting list?'),
    )
    others_get_involved = models.TextField(_('how others can get involved'),
        blank=True,
        null=True,
        help_text=_('How can others get involved in your project?'),
    )
    land_tenure_status = models.CharField(_('land tenure status'),
        choices=(
            ('owned', 'project owns the land'),
            ('licensed', 'project has a license for the land'),
            ('lease', 'project has a lease for the land'),
            ('access', 'project has access to the land'),
            ('not sure', "I'm not sure"),
        ),
        default='not sure',
        max_length=50,
        help_text=_('What is the land tenure status for the project? (This '
                    'will not be shared publicly.)'),
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
    name = models.CharField(_('name'), max_length=256)
    phone = models.CharField(_('phone'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('email'))
    type = models.ForeignKey('organize.OrganizerType')
    url = models.URLField(_('url'), null=True, blank=True)
    facebook_page = models.CharField(
        _('facebook page'),
        max_length=256,
        null=True,
        blank=True,
        help_text=('The Facebook page for your organization. Please do not '
                   'enter your personal Facebook page.'),
    )

    def __unicode__(self):
        return self.name


django_monitor.nq(StewardNotification)


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
        part_of_nga=instance.part_of_nga,
        support_organization=instance.support_organization,
        farm_stand=instance.farm_stand,
        waiting_list=instance.waiting_list,
        others_get_involved=instance.others_get_involved,
        land_tenure_status=instance.land_tenure_status,
    )
    steward_project.save()

    steward_project.content_object.known_use = steward_project.use
    steward_project.content_object.save()
