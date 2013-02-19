import geojson

from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView, DetailView
from django.views.generic.list import BaseListView, ListView


class GeoJSONResponseMixin(object):
    """A mixin that renders Places as GeoJSON."""
    response_class = HttpResponse

    def get_properties(self, place):
        """
        The properties that will be added to the given Place's GeoJSON feature.
        """
        return {
            'id': place.pk,
            'name': place.name,
            'popup_url': place.get_popup_url(),
        }

    def get_feature(self, place):
        """
        Get a Feature for a Place.
        """
        return geojson.Feature(
            place.id,
            geometry=geojson.Point(
                coordinates=(place.centroid.x, place.centroid.y)
            ),
            properties=self.get_properties(place),
        )

    def get_features(self):
        """
        Get a list of Features given our queryset.
        """
        try:
            places = [self.get_object(),]
        except Exception:
            places = self.get_queryset()
        return [self.get_feature(place) for place in places]

    def get_feature_collection(self):
        """
        Get a FeatureCollection for our Places.
        """
        return geojson.FeatureCollection(features=self.get_features())

    def render_to_response(self, context, **response_kwargs):
        """
        Render to GeoJSON.
        """
        return self.response_class(
            geojson.dumps(self.get_feature_collection()),
            mimetype='application/json',
        )


class GeoJSONListView(GeoJSONResponseMixin, BaseListView):
    pass


class GeoJSONDetailView(BaseDetailView, GeoJSONResponseMixin):
    pass


class DefaultTemplateMixin(TemplateResponseMixin):
    default_template_name = None

    def get_template_names(self):
        names = super(DefaultTemplateMixin, self).get_template_names()

        # fall back on default
        if self.default_template_name:
            names.append(self.default_template_name)
        return names


class AddAppModelMixin(object):
    app_name = None
    model_name = None

    def get_context_data(self, **kwargs):
        context = super(AddAppModelMixin, self).get_context_data(**kwargs)
        context.update({
            'app_name': self.app_name,
            'model': self.model,
            'model_name': self.model_name,
        })
        print context
        return context


class PlacesDetailView(AddAppModelMixin, DefaultTemplateMixin, DetailView):
    default_template_name = 'places/detail.html'


class PlacesPopupView(AddAppModelMixin, DefaultTemplateMixin, DetailView):
    default_template_name = 'places/popup.html'
    template_name_suffix='_popup'


class PlacesListView(AddAppModelMixin, DefaultTemplateMixin, ListView):
    default_template_name = 'places/list.html'


class PlacesGeoJSONListView(GeoJSONListView):
    pass


class PlacesGeoJSONDetailView(GeoJSONDetailView):
    pass
