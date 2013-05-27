from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from mailsender.helpers import (mail_multiple_personalized,
                                get_target_email_address)


def mass_mailing(subject, message, objects, template_name, **kwargs):
    messages = {}
    for obj in objects:
        # message gets sent once to each unique email address, thanks to dict
        messages[obj.email] = render_to_string(template_name, {
            'site': Site.objects.get_current(),
            'target': obj.content_object,
            'message': message,
            'obj': obj,
        })

    mail_multiple_personalized(subject, messages, **kwargs)


def mass_mail_watchers(subject, message, watchers, **kwargs):
    """
    Sends a message to watchers.
    """
    mass_mailing(
        subject,
        message,
        watchers,
        'organize/notifications/mass_watcher_text.txt',
        **kwargs
    )


def mass_mail_organizers(subject, message, organizers, **kwargs):
    """
    Sends a message to organizers.
    """
    mass_mailing(
        subject,
        message,
        organizers,
        'organize/notifications/mass_organizer_text.txt',
        **kwargs
    )


def mail_target_participants(participant_cls, target, subject,
                             excluded_emails=[], template=None, **kwargs):
    """Send a message to participants of a given target."""
    participants = participant_cls.objects.filter(
        content_type=ContentType.objects.get_for_model(target),
        object_id=target.pk,
    )
    participants = [p for p in participants if p.email not in excluded_emails]
    messages = _get_messages(participants, template, **kwargs)
    mail_multiple_personalized(subject, messages,
                               from_email=get_target_email_address(target))


def _get_messages(participants, template_name, **kwargs):
    messages = {}
    for p in participants:
        context = kwargs
        context.update({
            'BASE_URL': Site.objects.get_current().domain,
            'MAILREADER_REPLY_PREFIX': settings.MAILREADER_REPLY_PREFIX,
            'target': p.content_object,
            'participant': p,
        })
        messages[p.email] = render_to_string(template_name, context)
    return messages
