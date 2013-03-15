from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from organize.models import Organizer, Watcher


def mass_mailing(subject, message, objects, template_name, **kwargs):
    messages = {}
    for obj in objects:
        # message gets sent once to each unique email address, thanks to dict
        messages[obj.email] = render_to_string(template_name, {
            'BASE_URL': Site.objects.get_current().domain,
            'target': obj.target,
            'message': message,
            'obj': obj,
        })

    _mail_multiple_personalized(
        subject,
        messages,
        **kwargs
    )


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


def mail_facilitators(target, subject, message, excluded_emails=[],
                      is_note=False, url_suffix=''):
    """
    Sends a message to facilitators.
    """
    facilitators = settings.FACILITATORS['global']
    facilitators = [f for f in facilitators if f not in excluded_emails]

    messages = _get_facilitator_messages(
        facilitators,
        target,
        message,
        'organize/notifications/facilitators_text.txt',
        url_suffix,
        is_note=is_note,
    )
    _mail_multiple_personalized(subject, messages, fail_silently=False,
                                **_get_message_options(target, is_note=is_note))


def mail_target_organizers(target, subject, message, excluded_emails=[],
                           is_note=False, url_suffix=''):
    """
    Sends a message to organizers of a given target.
    """
    organizers = Organizer.objects.filter(
        target_type=ContentType.objects.get_for_model(target),
        target_id=target.pk,
    )
    organizers = [o for o in organizers if o.email not in excluded_emails]
    messages = _get_messages(
        organizers,
        message,
        'organize/notifications/organizers_text.txt',
        url_suffix,
        is_note=is_note,
    )
    _mail_multiple_personalized(subject, messages,
                                **_get_message_options(target, is_note=is_note))


def mail_target_watchers(target, subject, message, excluded_emails=[],
                         is_note=False, url_suffix=''):
    """
    Sends a message to watchers of a given target.
    """
    watchers = Watcher.objects.filter(
        target_type=ContentType.objects.get_for_model(target),
        target_id=target.pk,
    )
    watchers = [w for w in watchers if w.email not in excluded_emails]
    messages = _get_messages(
        watchers,
        message,
        'organize/notifications/watchers_text.txt',
        url_suffix,
        is_note=is_note,
    )
    _mail_multiple_personalized(subject, messages,
                                **_get_message_options(target, is_note=is_note))


def _get_messages(participants, detail_message, template_name, obj_url_suffix,
                  is_note=False):
    messages = {}
    for p in participants:
        messages[p.email] = render_to_string(template_name, {
            'BASE_URL': Site.objects.get_current().domain,
            'MAILREADER_REPLY_PREFIX': settings.MAILREADER_REPLY_PREFIX,
            'is_note': is_note,
            'target': p.target,
            'message': detail_message,
            'participant': p,
            'obj_url_suffix': obj_url_suffix,
        })
    return messages


def _get_facilitator_messages(facilitators, target, detail_message, template_name,
                              obj_url_suffix, is_note=False):
    messages = {}
    for facilitator in facilitators:
        messages[facilitator] = render_to_string(template_name, {
            'BASE_URL': Site.objects.get_current().domain,
            'MAILREADER_REPLY_PREFIX': settings.MAILREADER_REPLY_PREFIX,
            'is_note': is_note,
            'target': target,
            'message': detail_message,
            'obj_url_suffix': obj_url_suffix,
        })
    return messages


def _get_message_options(target, is_note=False):
    if not is_note: return {}
    return {
        'from_email': _get_target_email_address(target),
        'cc': None,
        'bcc': None,
    }


def _get_target_email_address(target):
    """
    Get the from email for the given target.
    """
    return 'FIXME'


def _mail_multiple_personalized(subject, messages, **kwargs):
    for email, message in messages.items():
        _mail_multiple(subject, message, [email], **kwargs)


def _mail_multiple(subject, message, email_addresses, from_email=None, cc=None,
                   bcc=None, html_message=None, connection=None,
                   fail_silently=True):
    """
    Sends a message to multiple email addresses. Based on
    django.core.mail.mail_admins()
    """
    for email_address in email_addresses:
        mail = EmailMultiAlternatives(
            u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
            message,
            bcc=bcc,
            cc=cc,
            connection=connection,
            from_email=from_email,
            to=[email_address],
        )
        if html_message:
            mail.attach_alternative(html_message, 'text/html')
        mail.send(fail_silently=fail_silently)
