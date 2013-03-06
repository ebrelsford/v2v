from django.conf.urls.defaults import include, patterns, url

from places.models import Place
from places.views import PlacesGeoJSONDetailView, PlacesGeoJSONListView,\
        PlacesDetailView, PlacesListView, PlacesPopupView


def make_place_patterns(app_name, model_name, model_class):
    return patterns('',

        url(r'^$',
            PlacesListView.as_view(
                app_name=app_name,
                model=model_class,
                model_name=model_name,
            ),
            name='%s_%s' % (app_name, model_name),
        ),

        # TODO make filterable
        url(r'^geojson',
            PlacesGeoJSONListView.as_view(
                model=model_class,
            ),
            name='%s_%s_geojson' % (app_name, model_name),
        ),

        url(r'^(?P<pk>\d+)/geojson/$',
            PlacesGeoJSONDetailView.as_view(
                model=model_class,
            ),
            name='%s_%s_detail_geojson' % (app_name, model_name),
        ),

        url(r'^(?P<pk>\d+)/$',
            PlacesDetailView.as_view(
                app_name=app_name,
                model=model_class,
                model_name=model_name,
            ),
            name='%s_%s_detail' % (app_name, model_name),
        ),

        url(r'^(?P<pk>\d+)/popup/$',
            PlacesPopupView.as_view(
                app_name=app_name,
                model=model_class,
                model_name=model_name,
                template_name_suffix='_popup'
            ),
            name='%s_%s_detail_popup' % (app_name, model_name),
        ),

    )

urlpatterns = patterns('',
)

for place_subclass in Place.__subclasses__():
    meta = place_subclass._meta

    app = meta.app_label.lower()
    model_name = meta.object_name.lower()

    urlpatterns += (
        url(r'%s/%s/' % (app, model_name),
            include(make_place_patterns(app, model_name, place_subclass))
        ),
    )
