import geojson

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, TemplateView

from inplace.views import GeoJSONListView

from organize.forms import OrganizerForm
from organize.views import EditParticipantMixin
from phillydata.parcels.models import Parcel
from phillydata.violations.models import Violation, ViolationLocation
from .models import Lot


class PlacesWithViolationsView(GeoJSONListView):

    def get_feature(self, parcel):
        violation = Violation.objects.filter(violation_location__point__within=parcel.geometry)[0]

        return geojson.Feature(
            parcel.id,
            geometry=geojson.MultiPolygon(
                coordinates=parcel.geometry.coords,
            ),
            properties={
                'type': violation.violation_type.code,
                'description': violation.violation_type.li_description,
            },
        )

    def get_queryset(self):
        parcels = [Parcel.objects.filter(geometry__contains_properly=loc.point)[0] for loc in ViolationLocation.objects.all()]
        pks = [p.pk for p in parcels]
        return Parcel.objects.filter(pk__in=pks)


class PlacesWithViolationsMap(TemplateView):
    template_name = 'lots/places_with_violations.html'

    #def get_context_data(self, **kwargs):
        #context = super(TemplateView, self).get_context_data(**kwargs)
        #return context


class LotsGeoJSON(GeoJSONListView):

    def get_feature(self, lot):
        try:
            owner_name = lot.owner.name
        except Exception:
            owner_name = 'unknown'

        return geojson.Feature(
            lot.pk,
            geometry=geojson.MultiPolygon(
                coordinates=lot.polygon.coords,
            ),
            properties={
                'is_available': lot.available_property is not None,
                'owner': owner_name,
            },
        )

    def get_queryset(self):
        return Lot.objects.all().select_related('owner', 'available_property')


class LotsMap(TemplateView):
    template_name = 'lots/map.html'


class EditLotParicipantView(EditParticipantMixin, TemplateView):
    template_name = 'lots/organize/edit_participant.html'

    def get_context_data(self, **kwargs):
        context = super(EditLotParicipantView, self).get_context_data(**kwargs)
        context.update({
            'email': self._get_email(context),
        })
        return context

    def get_participant_hash(self):
        return self.kwargs['hash']

    def _get_email(self, context):
        try:
            return context['organizers'][0].email
        except Exception:
            try:
                return context['watchers'][0].email
            except Exception:
                return None


class AddParticipantView(CreateView):
    form_class = OrganizerForm
    template_name = 'lots/organize/add_organizer.html'

    def get_context_data(self, **kwargs):
        context = super(AddParticipantView, self).get_context_data(**kwargs)
        context.update({
            'lot': Lot.objects.get(pk=self.kwargs['pk']),
        })
        return context

    def get_initial(self):
        initial = super(AddParticipantView, self).get_initial()
        try:
            target_id = self.kwargs['pk']
        except KeyError:
            raise Http404
        initial.update({
            'target_type': ContentType.objects.get_for_model(Lot),
            'target_id': target_id,
        })
        return initial

    def get_success_url(self):
        try:
            return reverse('lots:add_organizer_success',
                           kwargs={
                               'hash': self.object.email_hash[:9],
                               'pk': self.object.target_id,
                           })
        except Exception:
            raise Http404


class AddParticipantSuccessView(TemplateView):
    model = None
    template_name = 'lots/organize/add_organizer_success.html'

    def get_context_data(self, **kwargs):

        context = super(AddParticipantSuccessView, self).get_context_data(**kwargs)
        context['lot'] = get_object_or_404(Lot, pk=kwargs['pk'])
        try:
            context['participant'] = self.model.objects.filter(email_hash__istartswith=kwargs['hash'])[0]
        except Exception:
            raise Http404
        return context
