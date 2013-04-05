from django.contrib.contenttypes.models import ContentType
from django.views.generic import FormView, TemplateView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from feincms.content.application.models import app_reverse

from forms import MailParticipantsForm
from generic.views import JSONResponseView
from organize.mail import mass_mail_organizers, mass_mail_watchers
from organize.models import Organizer, Watcher
from lots.api import LotResource
from lots.models import Lot


class MailParticipantsView(LoginRequiredMixin, PermissionRequiredMixin,
                           FormView):

    form_class = MailParticipantsForm
    permission_required = ('organize.email_participants')
    template_name = 'extraadmin/mail_participants.html'

    # TODO validation--there have to be watchers or organizers selected!

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        participant_types = form.cleaned_data['participant_types']

        orm_filters = LotResource().build_filters(filters=self.request.POST)
        lot_pks = Lot.objects.filter(**orm_filters).values_list('pk', flat=True)

        if 'organizers' in participant_types:
            organizers = Organizer.objects.filter(
                content_type=ContentType.objects.get_for_model(Lot),
                object_id__in=lot_pks,
            ).distinct()
            organizers = organizers.exclude(email='')
            mass_mail_organizers(subject, message, organizers)
        if 'watchers' in participant_types:
            watchers = Watcher.objects.filter(
                content_type=ContentType.objects.get_for_model(Lot),
                object_id__in=lot_pks,
            )
            watchers = watchers.exclude(email='')
            mass_mail_watchers(subject, message, watchers)

        return super(MailParticipantsView, self).form_valid(form)

    def get_initial(self):
        initial = super(MailParticipantsView, self).get_initial()
        initial['participant_types'] = ('organizers', 'watchers',)
        return initial

    def get_success_url(self):
        return app_reverse('mail_participants_success', 'extraadmin.urls')


class MailParticipantsCountView(JSONResponseView):

    def get_context_data(self, **kwargs):
        orm_filters = LotResource().build_filters(filters=self.request.GET)
        lot_pks = Lot.objects.filter(**orm_filters).values_list('pk', flat=True)
        watcher_count = 0
        organizer_count = 0
        participant_types = self.request.GET.getlist('participant_types', [])
        if 'watchers' in participant_types:
            watcher_count = Watcher.objects.filter(
                content_type=ContentType.objects.get_for_model(Lot),
                object_id__in=lot_pks,
            ).distinct().count()
        if 'organizers' in participant_types:
            organizer_count = Organizer.objects.filter(
                content_type=ContentType.objects.get_for_model(Lot),
                object_id__in=lot_pks,
            ).distinct().count()
        return {
            'organizers': organizer_count,
            'watchers': watcher_count,
        }


class MailParticipantsSuccessView(LoginRequiredMixin, PermissionRequiredMixin,
                                  TemplateView):
    permission_required = ('organize.email_participants')
    template_name = 'extraadmin/mail_participants_success.html'
