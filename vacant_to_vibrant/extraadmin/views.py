from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Polygon
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import FormView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

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

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        participant_types = form.cleaned_data['participant_types']
        bbox = form.cleaned_data['bbox']

        # TODO owner type?
        filters = Q(
        )

        if bbox:
            p = Polygon.from_bbox(bbox.split(','))
            filters = filters & Q(lot__centroid__within=p)

        if 'organizers' in participant_types:
            organizers = Organizer.objects.filter(filters, email__isnull=False)
            organizers = organizers.exclude(email='')
            mass_mail_organizers(subject, message, organizers)
        if 'watchers' in participant_types:
            watchers = Watcher.objects.filter(filters, email__isnull=False)
            watchers = watchers.exclude(email='')
            mass_mail_watchers(subject, message, watchers)

        return super(MailParticipantsView, self).form_valid(form)


class MailParticipantsCountView(JSONResponseView):

    def get_context_data(self, **kwargs):
        orm_filters = LotResource().build_filters(filters=self.request.GET)
        lot_pks = Lot.objects.filter(**orm_filters).values_list('pk', flat=True)
        watcher_count = 0
        organizer_count = 0
        participant_types = self.request.GET.getlist('participant_types', [])
        if 'watchers' in participant_types:
            watcher_count = Watcher.objects.filter(
                target_type=ContentType.objects.get_for_model(Lot),
                target_id__in=lot_pks,
            ).distinct().count()
        if 'organizers' in participant_types:
            organizer_count = Organizer.objects.filter(
                target_type=ContentType.objects.get_for_model(Lot),
                target_id__in=lot_pks,
            ).distinct().count()
        return {
            'organizers': organizer_count,
            'watchers': watcher_count,
        }


@permission_required('organize.email_participants')
def mail_participants_done(request):
    return render_to_response('extraadmin/mail_participants_done.html', {},
                              context_instance=RequestContext(request))
