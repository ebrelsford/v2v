from datetime import date
import geojson
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic import CreateView, TemplateView

from forms_builder.forms.models import Form
from inplace.boundaries.models import Boundary
from inplace.views import (GeoJSONListView, KMLView, GeoJSONResponseMixin,
                           PlacesDetailView)

from files.forms import FileForm
from generic.views import CSVView, JSONResponseView
from notes.forms import NoteForm
from organize.forms import OrganizerForm, WatcherForm
from organize.models import Organizer, Watcher
from organize.notify import notify_participants_new_obj
from organize.views import EditParticipantMixin
from photos.forms import PhotoForm
from survey.forms import SurveyFormForForm
from survey.models import SurveyFormEntry
from .api import LotResource
from .forms import FiltersForm
from .models import Lot, Use


class FilteredLotsMixin(object):
    """A mixin that makes it easy to filter on Lots using a LotResource."""

    def get_lots(self):
        orm_filters = LotResource().build_filters(filters=self.request.GET)
        return Lot.objects.filter(**orm_filters)


class LotFieldsMixin(object):
    """
    A mixin that makes it easier to add a lot's fields to the view's output.
    """
    def get_fields(self):
        return self.fields

    def get_field_owner(self, lot):
        return lot.owner.name

    def get_field_owner_type(self, lot):
        return lot.owner.get_owner_type_display()

    def _field_value(self, lot, field):
        try:
            # Call get_field_<field>()
            return getattr(self, 'get_field_%s' % field)(lot)
        except AttributeError:
            try:
                # Else try to get the property from the model instance
                return getattr(lot, field)
            except AttributeError:
                return None

    def _as_dict(self, lot):
        return dict([(f, self._field_value(lot, f)) for f in self.fields])


class LotsCSV(LotFieldsMixin, FilteredLotsMixin, CSVView):
    fields = ('address_line1', 'city', 'state_province', 'postal_code',
              'latitude', 'longitude', 'known_use', 'owner', 'owner_type',)

    def get_filename(self):
        return 'Grounded lots %s' % date.today().strftime('%Y-%m-%d')

    def get_rows(self):
        for lot in self.get_lots():
            yield self._as_dict(lot)


class LotsKML(LotFieldsMixin, FilteredLotsMixin, KMLView):
    fields = ('address_line1', 'city', 'state_province', 'postal_code',
              'known_use', 'owner', 'owner_type',)

    def get_filename(self):
        return 'Grounded lots %s' % date.today().strftime('%Y-%m-%d')

    def get_context_data(self, **kwargs):
        return {
            'places': self.get_lots().kml(),
            'download': True,
            'filename': self.get_filename(),
        }

    def render_to_response(self, context):
        return super(LotsKML, self).render_to_response(context)


class LotsGeoJSON(LotFieldsMixin, FilteredLotsMixin, GeoJSONResponseMixin,
                  JSONResponseView):
    fields = ('address_line1', 'city', 'state_province', 'postal_code',
              'known_use', 'owner', 'owner_type',)

    def get_context_data(self, **kwargs):
        return self.get_feature_collection()

    def get_feature(self, lot):
        return geojson.Feature(
            lot.pk,
            geometry=json.loads(lot.centroid.geojson),
            properties=self._as_dict(lot),
        )

    def get_filename(self):
        return 'Grounded lots %s' % date.today().strftime('%Y-%m-%d')

    def get_queryset(self):
        return self.get_lots()

    def render_to_response(self, context):
        response = super(LotsGeoJSON, self).render_to_response(context)
        if self.request.GET.get('download', 'no') == 'yes':
            response['Content-Disposition'] = ('attachment; filename="%s.json"' %
                                               self.get_filename())
        return response


class LotsGeoJSONPolygon(GeoJSONListView):

    def _get_filters(self):
        return LotResource().build_filters(filters=self.request.GET)

    def get_feature(self, lot):
        return geojson.Feature(
            lot.pk,
            geometry=json.loads(lot.polygon.geojson),
            properties={
                'pk': lot.pk,
            },
        )

    def get_queryset(self):
        return Lot.objects.filter(polygon__isnull=False, **self._get_filters())


class LotsCountView(FilteredLotsMixin, JSONResponseView):

    def get_context_data(self, **kwargs):
        lots = self.get_lots()
        context = {
            'lots-count': lots.count(),
            'no-known-use-count': lots.filter(known_use=None).count()
        }
        for use in Use.objects.all():
            context['%s-count' % use.slug] = lots.filter(known_use=use).count()
        return context


class LotsCountBoundaryView(GeoJSONResponseMixin, JSONResponseView):

    def get_context_data(self, **kwargs):
        return self.get_features()

    def get_features(self):
        filters = LotResource().build_filters(filters=self.request.GET)

        try:
            # Ignore bbox
            del filters['centroid__within']
        except Exception:
            pass

        lots = Lot.objects.filter(**filters)

        # Get city council districts
        # TODO or use city_council_district field instead
        # TODO do this via a parameter
        boundaries = Boundary.objects.filter(
            layer__name='City Council Districts'
        )

        features = []
        for boundary in boundaries:
            features.append(geojson.Feature(
                boundary.pk,
                # TODO compress/simplify
                geometry=json.loads(boundary.geometry.geojson),
                properties={
                    'boundary_label': boundary.label,
                    'count': lots.filter(
                        centroid__within=boundary.geometry
                    ).count(),
                }
            ))
        return features


class LotsMap(TemplateView):
    template_name = 'lots/map.html'

    def get_context_data(self, **kwargs):
        context = super(LotsMap, self).get_context_data(**kwargs)
        context.update({
            'filters': FiltersForm(),
            'uses': Use.objects.all().order_by('name'),
        })
        return context


class LotDetailView(PlacesDetailView):
    model = Lot

    def get_context_data(self, **kwargs):
        form = Form.objects.get(pk=settings.LOT_SURVEY_FORM_PK)
        form_context = RequestContext(self.request, {
            'form': form,
        })

        initial = {
            'content_object': self.object,
        }
        form_kwargs = {}
        form_kwargs['initial'] = initial

        # Get the existing SurveyFormEntry for this lot, if any
        try:
            form_kwargs['instance'] = SurveyFormEntry.objects.get(
                content_type =ContentType.objects.get_for_model(self.object),
                object_id=self.object.pk,
            )
        except SurveyFormEntry.DoesNotExist:
            pass

        form_for_form = SurveyFormForForm(form, form_context, **form_kwargs)

        context = super(LotDetailView, self).get_context_data(**kwargs)
        context.update({
            'form': form_for_form,
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
        messages.success(self.request, '%s added successfully.' %
                         self._get_content_name())
        return self._get_lot().get_absolute_url()

    def get_template_names(self):
        return [
            'lots/content/add_%s.html' % self._get_content_name().lower(),
        ]

    def form_valid(self, form):
        """
        Save the content and notify participants who are following the target
        lot.
        """
        self.object = form.save()
        notify_participants_new_obj(self.object)
        return super(AddContentView, self).form_valid(form)


class AddFileView(AddContentView):
    form_class = FileForm


class AddNoteView(AddContentView):
    form_class = NoteForm


class AddPhotoView(AddContentView):
    form_class = PhotoForm
