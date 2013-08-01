from datetime import date
import geojson
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin

from forms_builder.forms import signals
from forms_builder.forms.models import Form
from inplace.boundaries.models import Boundary
from inplace.views import (GeoJSONListView, KMLView, GeoJSONResponseMixin,
                           PlacesDetailView)

from livinglots_usercontent.files.forms import FileForm
from livinglots_usercontent.notes.forms import NoteForm
from livinglots_usercontent.photos.forms import PhotoForm
from libapps.organize.notifications import notify_participants_new_obj
from libapps.organize.views import DeleteOrganizerView, EditParticipantMixin

from generic.views import CSVView, JSONResponseView, SuccessMessageFormMixin
from groundtruth.forms import GroundtruthRecordForm
from groundtruth.models import GroundtruthRecord
from monitor.views import MonitorMixin
from notify.views import NotifyFacilitatorsMixin
from phillyorganize.forms import OrganizerForm
from phillyorganize.models import Organizer
from steward.forms import StewardNotificationForm
from survey.forms import SurveyFormForForm
from survey.models import SurveyFormEntry
from .api import LotResource, VisibleLotResource
from .forms import FiltersForm
from .models import Lot, Use


#
# Helper mixins
#

class FilteredLotsMixin(object):
    """A mixin that makes it easy to filter on Lots using a LotResource."""

    def get_lots(self):
        # Give the user a different set of lots based on their permissions
        if self.request.user.has_perm('lots.view_all_lots'):
            resource = LotResource()
        else:
            resource = VisibleLotResource()
        orm_filters = resource.build_filters(filters=self.request.GET)
        return resource.apply_filters(self.request, orm_filters)


class LotContextMixin(ContextMixin):

    def get_lot(self):
        """Get the lot referred to by the incoming request"""
        try:
            if self.request.user.has_perm('lots.view_all_lots'):
                return Lot.objects.get(pk=self.kwargs['pk'])
            return Lot.visible.get(pk=self.kwargs['pk'])
        except Lot.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(LotContextMixin, self).get_context_data(**kwargs)
        context['lot'] = self.get_lot()
        return context


class LotAddGenericMixin(FormMixin):
    """
    A mixin that eases adding content that references a single lot using
    generic relationships.
    """

    def get_initial(self):
        """Add initial content_type and object_id to the form"""
        initial = super(LotAddGenericMixin, self).get_initial()
        try:
            object_id = self.kwargs['pk']
        except KeyError:
            raise Http404
        initial.update({
            'content_type': ContentType.objects.get_for_model(Lot),
            'object_id': object_id,
        })
        return initial


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

    def get_field_known_use(self, lot):
        return lot.known_use.name

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


class LotGeoJSONMixin(object):

    def get_feature(self, lot):
        if lot.known_use:
            layer = 'in use'
        elif lot.owner and lot.owner.owner_type == 'public':
            layer = 'public'
        elif lot.owner and lot.owner.owner_type == 'private':
            layer = 'private'
        else:
            layer = ''

        try:
            lot_geojson = lot.geojson
        except Exception:
            if lot.polygon:
                lot_geojson = lot.polygon.geojson
            else:
                lot_geojson = lot.centroid.geojson
        return geojson.Feature(
            lot.pk,
            geometry=json.loads(lot_geojson),
            properties={
                'pk': lot.pk,
                'layer': layer,
            },
        )


#
# Export views
#

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


class LotsGeoJSONPolygon(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_queryset(self):
        return self.get_lots().filter(polygon__isnull=False).geojson(
            field_name='polygon',
            precision=8,
        ).select_related('known_use', 'owner__owner_type')


class LotsGeoJSONCentroid(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_queryset(self):
        return self.get_lots().filter(centroid__isnull=False).geojson(
            field_name='centroid',
            precision=8,
        ).select_related('known_use', 'owner__owner_type')


#
# Counting views
#

class LotsCountView(FilteredLotsMixin, JSONResponseView):

    def get_context_data(self, **kwargs):
        lots = self.get_lots()
        context = {
            'lots-count': lots.count(),
            'no-known-use-count': lots.filter(known_use__isnull=True).count(),
            'in-use-count': lots.filter(
                known_use__isnull=False,
                known_use__visible=True,
            ).count(),
        }
        return context


class LotsCountBoundaryView(JSONResponseView):

    def get_context_data(self, **kwargs):
        return self.get_counts()

    def get_lot_resource(self):
        if self.request.user.has_perm('lots.view_all_lots'):
            return LotResource()
        return VisibleLotResource()

    def get_counts(self):
        boundary_layer = self.request.GET.get('choropleth_boundary_layer', '')
        lot_resource = self.get_lot_resource()
        filters = lot_resource.build_filters(filters=self.request.GET)

        try:
            # Ignore bbox
            del filters['centroid__within']
        except Exception:
            pass

        lots = lot_resource.apply_filters(self.request, filters)

        boundaries = Boundary.objects.filter(
            layer__name=boundary_layer,
        )

        counts = {}
        for boundary in boundaries:
            counts[boundary.label] = lots.filter(
                centroid__within=boundary.simplified_geometry
            ).count()
        return counts


class LotsMap(TemplateView):
    template_name = 'lots/map.html'

    def get_context_data(self, **kwargs):
        context = super(LotsMap, self).get_context_data(**kwargs)
        context.update({
            'filters': FiltersForm(),
            'uses': Use.objects.all().order_by('name'),
        })
        return context


#
# Detail views
#

class LotDetailView(PlacesDetailView):
    model = Lot

    def get_object(self):
        lot = super(LotDetailView, self).get_object()
        if not (lot.is_visible or self.request.user.has_perm('lots.view_all_lots')):
            raise Http404
        return lot

    def get(self, request, *args, **kwargs):
        # Redirect to the lot's group, if it has one
        self.object = self.get_object()
        if self.object.group:
            messages.info(request, _("The lot you requested is part of a "
                                     "group. Here is the group's page."))
            return HttpResponseRedirect(self.object.group.get_absolute_url())
        return super(LotDetailView, self).get(request, *args, **kwargs)


class LotGeoJSONDetailView(LotGeoJSONMixin, GeoJSONListView):
    model = Lot

    def get_queryset(self):
        lot = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return self.model.objects.find_nearby(lot, include_self=True, miles=.1)


#
# Survey views
#

class EditLandCharacteristicsSurvey(SuccessMessageFormMixin, LotContextMixin,
                                    FormView):
    form_class = SurveyFormForForm
    success_message = _('Successfully updated survey.')
    template_name = 'lots/survey/land_survey.html'

    def get_form(self, form_class):
        survey_form = self.get_survey_form()
        form_context = RequestContext(self.request, {
            'form': survey_form,
        })
        return form_class(survey_form, form_context, **self.get_form_kwargs())

    def form_invalid(self, form):
        signals.form_invalid.send(sender=self.request, form=form)
        return super(EditLandCharacteristicsSurvey, self).form_invalid(form)

    def form_valid(self, form):
        entry = form.save()
        self.content_object = entry.content_object
        signals.form_valid.send(sender=self.request, form=form, entry=entry)
        return super(EditLandCharacteristicsSurvey, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditLandCharacteristicsSurvey, self).get_context_data(**kwargs)
        context['survey_form_pk'] = settings.LOT_SURVEY_FORM_PK
        return context

    def get_success_url(self):
        return self.get_lot().get_absolute_url()

    def get_initial(self):
        return {
            'content_object': self.get_lot(),
            'survey_form': self.get_survey_form(),
        }

    def get_survey_form(self):
        try:
            return self.survey_form
        except Exception:
            self.survey_form = Form.objects.get(pk=settings.LOT_SURVEY_FORM_PK)
            return self.survey_form

    def get_form_kwargs(self):
        kwargs = super(EditLandCharacteristicsSurvey, self).get_form_kwargs()

        # Get the existing SurveyFormEntry for this lot, if any
        try:
            lot = self.get_lot()
            kwargs['instance'] = SurveyFormEntry.objects.filter(
                content_type=ContentType.objects.get_for_model(lot),
                object_id=lot.pk,
                survey_form=self.get_survey_form(),
            ).order_by('-entry_time')[0]
        except IndexError:
            pass

        return kwargs


#
# Participant views
#

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


class AddParticipantView(LotAddGenericMixin, LotContextMixin, ParticipantMixin,
                         CreateView):

    def get_form_class(self):
        if self.model is Organizer:
            return OrganizerForm

    def get_success_url(self):
        try:
            return reverse('lots:add_%s_success' % self._get_participant_type(),
                           kwargs={
                               'lot_pk': self.object.object_id,
                               'hash': self.object.email_hash[:30],
                               'pk': self.object.pk,
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
        lot = get_object_or_404(Lot, pk=kwargs['lot_pk'])

        context = super(AddParticipantSuccessView, self).get_context_data(**kwargs)
        context['lot'] = lot
        try:
            context['participant'] = self.model.objects.filter(
                object_id=lot.pk,
                email_hash__istartswith=kwargs['hash'],
                pk=self.kwargs['pk'],
            )[0]
        except Exception:
            raise Http404
        return context

    def get_template_names(self):
        return [
            'lots/organize/add_%s_success.html' % self._get_participant_type(),
        ]


class DeletePhillyOrganizerView(DeleteOrganizerView):
    template_name = 'lots/organize/organizer_confirm_delete.html'

    def get_object(self, **kwargs):
        try:
            return Organizer.objects.get(
                object_id=self.kwargs['lot_pk'],
                email_hash__istartswith=self.kwargs['hash'],
                pk=self.kwargs['pk'],
            )
        except Exception:
            raise Http404('Could not find the lot you were looking for.')

    def _get_success_message(self):
        return _('You are no longer subscribed to %s' % self.object.content_object)


#
# Steward views
#

class AddStewardNotificationView(SuccessMessageFormMixin, LotAddGenericMixin,
                                 LotContextMixin, MonitorMixin,
                                 NotifyFacilitatorsMixin, CreateView):
    form_class = StewardNotificationForm
    success_message = _('Your information has been added to the system and '
                        'will appear once an administrator looks over it.')
    template_name = 'lots/steward/stewardnotification_add.html'

    def get_should_notify_facilitators(self, obj):
        # Don't bother notifying facilitators of the object was auto-moderated
        # and approved
        return self.should_notify_facilitators and not obj.is_approved

    def get_success_url(self):
        try:
            return reverse('lots:add_stewardnotification_success',
                           kwargs={
                               'pk': self.object.object_id,
                           })
        except Exception:
            raise Http404


class AddStewardNotificationSuccessView(TemplateView):
    template_name = 'lots/steward/stewardnotification_add_success.html'

    def get_context_data(self, **kwargs):
        context = super(AddStewardNotificationSuccessView, self).get_context_data(**kwargs)
        context['lot'] = get_object_or_404(Lot, pk=kwargs['pk'])
        return context


#
# Groundtruth views
#

class AddGroundtruthRecordView(LotAddGenericMixin, LotContextMixin,
                               MonitorMixin, SuccessMessageFormMixin,
                               NotifyFacilitatorsMixin, CreateView):
    form_class = GroundtruthRecordForm
    template_name = 'lots/groundtruth/groundtruthrecord_add.html'

    def get_initial(self):
        initial = super(AddGroundtruthRecordView, self).get_initial()
        initial['use'] = Use.objects.get(visible=False, name='other (default)')
        return initial

    def get_success_message(self):
        if self.object.is_approved:
            return _('Lot updated with your correction.')
        else:
            return _('Thanks for your correction. The lot will be updated '
                     'once we have a chance to look at it.')

    def get_should_notify_facilitators(self, obj):
        # Don't bother notifying facilitators of the object was auto-moderated
        # and approved
        return self.should_notify_facilitators and not obj.is_approved

    def get_success_url(self):
        try:
            return reverse('lots:lot_detail',
                           kwargs={
                               'pk': self.object.object_id,
                           })
        except Exception:
            raise Http404


class AddGroundtruthRecordSuccessView(TemplateView):
    template_name = 'lots/groundtruth/groundtruthrecord_add_success.html'

    def get_context_data(self, **kwargs):
        context = super(AddGroundtruthRecordSuccessView, self).get_context_data(**kwargs)
        context['lot'] = get_object_or_404(Lot, pk=kwargs['pk'])
        context['groundtruth_record'] = get_object_or_404(
            GroundtruthRecord,
            pk=kwargs['record_pk']
        )
        return context


#
# Content views
#

class AddContentView(SuccessMessageFormMixin, LotAddGenericMixin,
                     LotContextMixin, CreateView):

    def _get_content_name(self):
        return self.form_class._meta.model._meta.object_name

    def get_success_message(self):
        return '%s added successfully.' % self._get_content_name()

    def get_success_url(self):
        return self.get_lot().get_absolute_url()

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
