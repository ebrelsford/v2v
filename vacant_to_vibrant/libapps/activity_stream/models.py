from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.contrib.contenttypes.models import ContentType

from actstream import settings as actstream_settings
from actstream.actions import now
from actstream.exceptions import check_actionable_model
from actstream.models import Action

from .signals import action


def place_action_handler(verb, **kwargs):
    """
    Handler function to create Action instance upon action signal call.
    """
    kwargs.pop('signal', None)

    actor = kwargs.pop('sender', None)
    if not actor:
        actor = User.objects.get(pk=settings.ACTIVITY_STREAM_DEFAULT_ACTOR_PK)
    check_actionable_model(actor)

    newaction = Action(
        actor_content_type=ContentType.objects.get_for_model(actor),
        actor_object_id=actor.pk,
        verb=unicode(verb),
        place=kwargs.pop('place', None),
        public=bool(kwargs.pop('public', True)),
        description=kwargs.pop('description', None),
        timestamp=kwargs.pop('timestamp', now())
    )

    for opt in ('target', 'action_object'):
        obj = kwargs.pop(opt, None)
        if not obj is None:
            check_actionable_model(obj)
            setattr(newaction, '%s_object_id' % opt, obj.pk)
            setattr(newaction, '%s_content_type' % opt,
                    ContentType.objects.get_for_model(obj))

    if actstream_settings.USE_JSONFIELD and len(kwargs):
        newaction.data = kwargs
    newaction.save()


# Use our action handler instead
action.disconnect(dispatch_uid='actstream.models')
action.connect(place_action_handler, dispatch_uid='activity_stream.models')

# Make Action.place available
PointField(blank=True, null=True).contribute_to_class(Action, 'place')


# Add receivers for creating actions
from django.db.models.signals import post_save
from django.dispatch import receiver

from libapps.content.files.models import File
from libapps.content.notes.models import Note
from libapps.content.photos.models import Photo

from phillyorganize.models import Organizer, Watcher

from .signals import action


def _add_action(sender, verb, created=False, instance=None, **kwargs):
    if not instance or not created: return
    action.send(
        sender,
        verb=verb,
        action_object=instance, # action object, what was created
        place=instance.content_object.centroid, # where did it happen?
        target=instance.content_object, # what did it happen to?
        data={},
    )


@receiver(post_save, sender=Organizer, dispatch_uid='activity_stream.organizer')
def add_organizer_action(sender, instance=None, **kwargs):
    if not instance: return
    _add_action(instance, 'started organizing', instance=instance, **kwargs)


@receiver(post_save, sender=Watcher, dispatch_uid='activity_stream.watcher')
def add_action(sender, instance=None, **kwargs):
    if not instance: return
    _add_action(instance, 'started watching', instance=instance, **kwargs)


@receiver(post_save, sender=Note, dispatch_uid='activity_stream.note')
def add_note_action(sender, instance=None, **kwargs):
    print 'note added:', instance
    if not instance: return
    _add_action(instance.added_by, 'wrote', instance=instance, **kwargs)


@receiver(post_save, sender=Photo, dispatch_uid='activity_stream.photo')
def add_photo_action(sender, instance=None, **kwargs):
    if not instance: return
    _add_action(instance.added_by, 'posted a picture', instance=instance,
                **kwargs)


@receiver(post_save, sender=File, dispatch_uid='activity_stream.file')
def add_file_action(sender, instance=None, **kwargs):
    if not instance: return
    _add_action(instance.added_by, 'posted a file', instance=instance,
                **kwargs)
