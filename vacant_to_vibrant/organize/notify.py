from django.conf import settings
from django.core.mail import mail_managers
from django.template.loader import render_to_string

from .mail import (mail_target_organizers, mail_target_watchers,
                   mail_facilitators)


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

    template = ('organize/notifications/facilitators_new_%s.txt' %
                obj._meta.object_name.lower())
    subject = 'Lot updated--new %s' % obj._meta.object_name
    mail_facilitators(target, subject, template=template, **kwargs)


def notify_organizers_and_watchers(obj):
    """
    Send Organizers and Watchers a notification that the given obj was added
    to its target.
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

    organizers_template = ('organize/notifications/organizers_new_%s.txt' %
                           obj._meta.object_name.lower())
    organizers_subject = 'Organized %s updated!' % target._meta.object_name
    mail_target_organizers(target, organizers_subject,
                           template=organizers_template, **kwargs)

    watchers_template = ('organize/notifications/watchers_new_%s.txt' %
                           obj._meta.object_name.lower())
    watchers_subject = 'Watched %s updated!' % target._meta.object_name
    mail_target_watchers(target, watchers_subject,
                         template=watchers_template, **kwargs)
