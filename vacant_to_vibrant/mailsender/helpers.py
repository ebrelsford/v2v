from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.contrib.sites.models import Site


def mail_multiple_personalized(subject, messages, **kwargs):
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


def get_target_email_address(target):
    """Get the from email for the given target."""
    site = Site.objects.get_current()
    target_name = target._meta.object_name
    return '"%s %s %d" <%s+%d@%s>' % (
        site.name,
        target_name.title(),
        target.pk,

        target_name.lower(),
        target.pk,
        site.domain,
    )
