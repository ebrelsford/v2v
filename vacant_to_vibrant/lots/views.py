import geojson
import json

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, TemplateView

from inplace.views import GeoJSONListView

from files.forms import FileForm
from generic.views import JSONResponseView
from notes.forms import NoteForm
from organize.forms import OrganizerForm, WatcherForm
from organize.models import Organizer, Watcher
from organize.views import EditParticipantMixin
from phillydata.parcels.models import Parcel
from phillydata.violations.models import Violation, ViolationLocation
from photos.forms import PhotoForm
from .api import LotResource
from .forms import FiltersForm
from .models import Lot, Use


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

    def _get_filters(self):
        print self.request.GET
        return {}

    def get_feature(self, lot):
        return geojson.Feature(
            lot.pk,
            geometry=json.loads(lot.centroid.geojson),
            properties={},
        )

    def get_queryset(self):
        #organized_lot_pks = Organizer.objects.all().values_list('object_id', flat=True)
        #return Lot.objects.filter(pk__in=organized_lot_pks)

        self._get_filters()
        return Lot.objects.all()
        #return Lot.objects.filter(pk=65667)
        #return Lot.objects.all().select_related('owner', 'available_property')


class LotsCountView(JSONResponseView):

    def get_context_data(self, **kwargs):
        orm_filters = LotResource().build_filters(filters=self.request.GET)
        lots = Lot.objects.filter(**orm_filters)
        context = {
            'lots-count': lots.count(),
            'no-known-use-count': lots.filter(known_use=None).count()
        }
        for use in Use.objects.all():
            context['%s-count' % use.slug] = lots.filter(known_use=use).count()
        return context


class LotsMap(TemplateView):
    template_name = 'lots/map.html'

    def get_context_data(self, **kwargs):
        context = super(LotsMap, self).get_context_data(**kwargs)
        context.update({
            'filters': FiltersForm(),
            'uses': Use.objects.all().order_by('name'),
        })
        return context


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


class ParticipantMixin(object):

    def _get_participant_type(self):
        return self.model._meta.object_name.lower()


class AddParticipantView(ParticipantMixin, CreateView):

    def get_context_data(self, **kwargs):
        context = super(AddParticipantView, self).get_context_data(**kwargs)
        context.update({
            'lot': Lot.objects.get(pk=self.kwargs['pk']),
        })
        return context

    def get_form_class(self):
        if self.model is Organizer:
            return OrganizerForm
        elif self.model is Watcher:
            return WatcherForm

    def get_initial(self):
        initial = super(AddParticipantView, self).get_initial()
        try:
            object_id = self.kwargs['pk']
        except KeyError:
            raise Http404
        initial.update({
            'content_type': ContentType.objects.get_for_model(Lot),
            'object_id': object_id,
        })
        return initial

    def get_success_url(self):
        try:
            return reverse('lots:add_%s_success' % self._get_participant_type(),
                           kwargs={
                               'hash': self.object.email_hash[:30],
                               'pk': self.object.object_id,
                           })
        except Exception:
            raise Http404

    def get_template_names(self):
        return [
            'lots/organize/add_%s.html' % self._get_participant_type(),
        ]


class AddParticipantSuccessView(ParticipantMixin, TemplateView):
    model = None

    def get_context_data(self, **kwargs):

        context = super(AddParticipantSuccessView, self).get_context_data(**kwargs)
        context['lot'] = get_object_or_404(Lot, pk=kwargs['pk'])
        try:
            context['participant'] = self.model.objects.filter(
                email_hash__istartswith=kwargs['hash']
            )[0]
        except Exception:
            raise Http404
        return context

    def get_template_names(self):
        return [
            'lots/organize/add_%s_success.html' % self._get_participant_type(),
        ]


class AddContentView(CreateView):

    def _get_lot(self):
        try:
            return Lot.objects.get(pk=self.kwargs['pk'])
        except Exception:
            raise Http404

    def _get_content_name(self):
        return self.form_class._meta.model._meta.object_name

    def get_context_data(self, **kwargs):
        context = super(AddContentView, self).get_context_data(**kwargs)
        context.update({
            'lot': self._get_lot(),
        })
        return context

    def get_initial(self):
        initial = super(AddContentView, self).get_initial()
        try:
            object_id = self.kwargs['pk']
        except KeyError:
            raise Http404
        initial.update({
            'content_type': ContentType.objects.get_for_model(Lot),
            'object_id': object_id,
        })
        return initial

    def get_success_url(self):
        messages.info(self.request, '%s added successfully.' %
                      self._get_content_name())
        return self._get_lot().get_absolute_url()

    def get_template_names(self):
        return [
            'lots/content/add_%s.html' % self._get_content_name().lower(),
        ]


class AddFileView(AddContentView):
    form_class = FileForm


class AddNoteView(AddContentView):
    form_class = NoteForm


class AddPhotoView(AddContentView):
    form_class = PhotoForm
