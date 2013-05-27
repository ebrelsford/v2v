from .mail import mail_target_participants
from .models import get_participant_models


def notify_participant_type_new_obj(participant_class, obj):
    target = obj.content_object
    if not target: return

    kwargs = {
        'obj': obj,
    }
    try:
        kwargs['excluded_emails'] = [obj.email]
    except Exception:
        kwargs['excluded_emails'] = []

    template = 'organize/notifications/%ss/new_%s.txt' % (
        participant_class.__name__.lower(),
        obj._meta.object_name.lower()
    )
    subject = '%s %s updated!' % (
        participant_class.participation_adjective().title(),
        target._meta.object_name.lower(),
    )
    mail_target_participants(participant_class, target, subject,
                             template=template, **kwargs)


def notify_participants_new_obj(obj):
    for participant_cls in get_participant_models():
        notify_participant_type_new_obj(participant_cls, obj)
