from datetime import datetime, timedelta
from itertools import groupby
import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string

from .models import DeliveryRecord


class Mailer(object):

    def __init__(self, mailing):
        self.mailing = mailing
        self.last_checked = self.mailing.last_checked
        self.time_started = datetime.now()

        self.mailing.last_checked = self.time_started
        self.mailing.save()

    def get_recipients(self):
        """Get the recipients to which this mailing should be sent."""
        return ()

    def get_already_received(self, receiver_type=None):
        """
        Find entities [of a particular type] that already received the mailing.
        """
        drs = DeliveryRecord.objects.filter(
            sent=True,
            mailing=self.mailing,
        )
        if receiver_type:
            drs = drs.filter(receiver_type=receiver_type)

        # XXX this is not very efficient
        return [r.receiver_object for r in drs if r.receiver_object is not None]

    def get_context(self, recipients):
        """
        Get the context to be used when constructing the subject and text of
        the mailing.
        """
        return {
            'mailing': self.mailing,
            'recipients': recipients,
        }

    def build_subject(self, recipients, context):
        return render_to_string(self.mailing.subject_template_name, context)

    def build_message(self, recipients, context):
        return render_to_string(self.mailing.text_template_name, context)

    def build_bcc(self, recipients):
        """Get a list of email addresses to BCC."""
        return (settings.FACILITATORS.get('global', []))

    def add_delivery_records(self, recipients, sent=True):
        """
        Add a DeliveryRecord to each recipient.
        """
        drs = []
        for recipient in recipients:
            dr = DeliveryRecord(
                sent=sent,
                mailing=self.mailing,
                receiver_object=recipient
            )
            dr.save()
            drs.append(dr)
        return drs

    def mail(self, fake=False):
        """Get intended recipients, prepare the message, send it."""
        recipients = self.get_recipients()

        # Faking it--just add delivery records for recipients and jump out
        if fake:
            self.add_delivery_records(recipients)
            return recipients

        duplicate_handling = self.mailing.duplicate_handling
        if duplicate_handling in ('merge', 'send first'):
            # group by email address to handle duplicates
            for email, recipient_group in groupby(recipients, lambda r: r.email):
                if duplicate_handling == 'send first':
                    recipient_group = [recipient_group[0]]
                self._prepare_and_send_message(list(recipient_group), email)
        else:
            # Don't bother grouping--every recipient gets every message
            for r in recipients:
                self._prepare_and_send_message([r], r.email)
        return recipients

    def _prepare_and_send_message(self, recipients, email):
        """
        Build the subject and text of the message, email it to the given
        email address.
        """
        context = self.get_context(recipients)
        self._send(
            self.build_subject(recipients, context),
            self.build_message(recipients, context),
            email,
            bcc=self.build_bcc(recipients),
        )
        return self.add_delivery_records(recipients)

    def _send(self, subject, message, email_address,
              bcc=[settings.FACILITATORS['global']], connection=None,
              fail_silently=True):
        # Subject cannot contain newlines
        subject = subject.replace('\n', '').strip()

        logging.debug('sending mail with subject "%s" to %s'
                      % (subject, email_address))
        logging.debug('bcc: %s' % (bcc,))
        logging.debug('full text: "%s"' % message)

        mail = EmailMessage(
            u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
            message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_address],
            connection=connection,
            bcc=bcc,
        )
        mail.send(fail_silently=fail_silently)


class DaysAfterAddedMailer(Mailer):

    def get_recipient_queryset(self, model):
        """
        Check for entities added in the time between the last time the mailing
        was sent and now, shifting backward in time for the number of days
        after an entity is added that we want to send them the mailing.
        """
        delta = timedelta(days=self.mailing.days_after_added)
        return model.objects.filter(
            added__gt=self.last_checked - delta,
            added__lte=self.time_started - delta,
            email__isnull=False,
        ).exclude(email='')

    def _get_ctype_recipients(self, ctype):
        """Get entities of type ctype that should receive the mailing."""
        type_recipients = self.get_recipient_queryset(ctype.model_class())

        # only get already received if there are potential recipients
        if not type_recipients:
            return []

        received = self.get_already_received(receiver_type=ctype)

        return list(set(type_recipients) - set(received))

    def get_recipients(self):
        recipient_lists = [self._get_ctype_recipients(ct) for ct in self.mailing.target_types.all()]
        return reduce(lambda x,y: x+y, recipient_lists)

    def get_context(self, recipients):
        context = super(DaysAfterAddedMailer, self).get_context(recipients)
        context['has_received_this_mailing'] = self.has_received(
            self.mailing,
            recipients[0]
        )
        return context

    def has_received(self, mailing, recipient):
        other_pks = recipient.__class__.objects.filter(
            email=recipient.email
        ).exclude(pk=recipient.pk).values_list('pk', flat=True)

        records = DeliveryRecord.objects.filter(
            mailing=mailing,
            receiver_object_id__in=other_pks,
            receiver_type=ContentType.objects.get_for_model(recipient)
        )
        return records.count() > 0


class DaysAfterParticipantAddedMailer(DaysAfterAddedMailer):
    """
    DaysAfterAddedMailer customized for participants.
    """

    def get_context(self, recipients):
        context = super(DaysAfterParticipantAddedMailer, self).get_context(recipients)

        # Add BASE_URL for full-path links back to the site
        context['BASE_URL'] = Site.objects.get_current().domain

        # Consolidate participant objects (handy when merging mailings)
        context['lots'] = [r.content_object for r in recipients]

        # Url for changing what one's organizing/watching
        context['edit_url'] = recipients[0].get_edit_url()
        return context
