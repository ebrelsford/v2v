from django.conf import settings
from django.core.mail import mail_managers
from django.template.loader import render_to_string

from .mail import mail_target_participants, mail_facilitators
from .models import get_participant_models


def notify_managers(obj):
    obj_model_name = obj._meta.object_name.lower()
    template_dir = 'organize/notifications'
    subject_template_name = '%s/managers_new_%s_subject.txt' % (template_dir,
                                                                obj_model_name)
    text_template_name = '%s/managers_new_%s_text.txt' % (template_dir,
                                                          obj_model_name)

    subject = render_to_string(subject_template_name).strip()
    message = render_to_string(text_template_name, {
        'obj': obj,
        'BASE_URL': settings.BASE_URL,
    })
    mail_managers(subject, message)


def notify_facilitators(obj):
    """
    Send facilitators updates.
    """
    target = obj.content_object
    if not target: return

    kwargs = {
        'obj': obj,
    }
    try:
        kwargs['excluded_emails'] = [obj.email]
    except Exception:
        kwargs['excluded_emails'] = []

    template = ('organize/notifications/facilitators/new_%s.txt' %
                obj._meta.object_name.lower())
    subject = '%s updated--new %s' % (obj.content_object._meta.object_name,
                                      obj._meta.object_name)
    mail_facilitators(target, subject, template=template, **kwargs)


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
