from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string


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

    _mail_multiple_personalized(subject, messages, **kwargs)


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


def mail_facilitators(target, subject, excluded_emails=[],
                      template='organize/notifications/facilitators_text.txt',
                      **kwargs):
    """Sends a message to facilitators."""
    facilitators = settings.FACILITATORS['global']
    facilitators = [f for f in facilitators if f not in excluded_emails]

    messages = _get_facilitator_messages(facilitators, target, template,
                                         **kwargs)
    _mail_multiple_personalized(subject, messages, fail_silently=False,
                                **_get_message_options(target))


def mail_target_participants(participant_cls, target, subject,
                             excluded_emails=[], template=None, **kwargs):
    """Send a message to participants of a given target."""
    participants = participant_cls.objects.filter(
        content_type=ContentType.objects.get_for_model(target),
        object_id=target.pk,
    )
    participants = [p for p in participants if p.email not in excluded_emails]
    messages = _get_messages(participants, template, **kwargs)
    _mail_multiple_personalized(subject, messages,
                                **_get_message_options(target))


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


def _get_facilitator_messages(facilitators, target, template_name, **kwargs):
    messages = {}
    for facilitator in facilitators:
        context = kwargs
        context.update({
            'BASE_URL': Site.objects.get_current().domain,
            'MAILREADER_REPLY_PREFIX': settings.MAILREADER_REPLY_PREFIX,
            'target': target,
        })
        messages[facilitator] = render_to_string(template_name, context)
    return messages


def _get_message_options(target):
    return {
        'from_email': _get_target_email_address(target),
        'cc': None,
        'bcc': None,
    }


def _get_target_email_address(target):
    """Get the from email for the given target."""
    site = Site.objects.get_current()
    target_name = target._meta.object_name
    return '"%s %s %d" <%s-%d@%s>' % (
        site.name,
        target_name.title(),
        target.pk,

        target_name.lower(),
        target.pk,
        site.domain,
    )


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
