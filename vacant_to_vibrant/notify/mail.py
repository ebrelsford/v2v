from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from mailsender.helpers import (mail_multiple_personalized,
                                get_target_email_address)


def mail_facilitators(target, subject, excluded_emails=[],
                      template='organize/notifications/facilitators_text.txt',
                      **kwargs):
    """Sends a message to facilitators."""
    facilitators = settings.FACILITATORS['global']
    facilitators = [f for f in facilitators if f not in excluded_emails]

    messages = _get_facilitator_messages(facilitators, target, template,
                                         **kwargs)
    mail_multiple_personalized(subject, messages, fail_silently=False,
                               from_email=get_target_email_address(target))


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
