from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from libapps.organize.mail import mass_mail_organizers
from phillyorganize.models import Organizer

from forms import MailParticipantsForm
from generic.views import JSONResponseView
from lots.api import LotResource
from lots.models import Lot


class MailParticipantsView(LoginRequiredMixin, PermissionRequiredMixin,
                           FormView):

    form_class = MailParticipantsForm
    permission_required = ('organize.email_participants')
    template_name = 'extraadmin/mail_participants.html'

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        filters = form.cleaned_data['filters']

        resource = LotResource()
        orm_filters = resource.build_filters(filters=filters)
        lot_pks = resource.apply_filters(self.request, orm_filters).values_list('pk', flat=True)

        participant_types = orm_filters.get('participant_types', [])

        if 'organizers' in participant_types:
            self._mail_organizers(lot_pks, subject, message)

        return super(MailParticipantsView, self).form_valid(form)

    def get_initial(self):
        initial = super(MailParticipantsView, self).get_initial()
        initial['participant_types'] = ('organizers',)
        return initial

    def get_success_url(self):
        return reverse('extraadmin:mail_participants_success')

    def _mail_organizers(self, lot_pks, subject, message):
        organizers = Organizer.objects.filter(
            content_type=ContentType.objects.get_for_model(Lot),
            object_id__in=lot_pks,
        ).distinct()
        organizers = organizers.exclude(email='')
        mass_mail_organizers(subject, message, organizers)


class MailParticipantsCountView(JSONResponseView):

    def get_context_data(self, **kwargs):
        participant_types = self._get_participant_types()
        lot_pks = self.get_lots().values_list('pk', flat=True)
        return {
            'organizers': self._get_organizer_count(participant_types, lot_pks),
        }

    def get_lots(self):
        resource = LotResource()
        orm_filters = resource.build_filters(filters=self.request.GET)
        return resource.apply_filters(self.request, orm_filters)

    def _get_participant_types(self):
        return self.request.GET.getlist('participant_types', [])

    def _get_organizer_count(self, participant_types, lot_pks):
        organizer_count = 0
        if 'organizers' in participant_types:
            organizer_count = Organizer.objects.filter(
                content_type=ContentType.objects.get_for_model(Lot),
                object_id__in=lot_pks,
            ).distinct().count()
        return organizer_count


class MailParticipantsSuccessView(LoginRequiredMixin, PermissionRequiredMixin,
                                  TemplateView):
    permission_required = ('organize.email_participants')
    template_name = 'extraadmin/mail_participants_success.html'


class ExtraAdminIndex(LoginRequiredMixin, PermissionRequiredMixin,
                      TemplateView):
    # Either require ALL permissions required to perform actions on this page
    # or require ONE of them, filter template accordingly
    permission_required = ('organize.email_participants',)
    template_name = 'extraadmin/index.html'
