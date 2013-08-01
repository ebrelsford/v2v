from django.conf.urls.defaults import patterns, url

from phillyorganize.models import Organizer

from .views import (LotDetailView, LotGeoJSONDetailView, EditLotParicipantView,
                    AddParticipantView, LotsGeoJSON, LotsGeoJSONPolygon,
                    LotsGeoJSONCentroid, AddParticipantSuccessView,
                    DeletePhillyOrganizerView, AddStewardNotificationView,
                    AddStewardNotificationSuccessView,
                    AddGroundtruthRecordView,
                    AddPhotoView, AddNoteView, AddFileView, LotsCountView,
                    LotsCountBoundaryView, LotsCSV, LotsKML,
                    EditLandCharacteristicsSurvey)


urlpatterns = patterns('',
    url(r'^csv/', LotsCSV.as_view(), name='csv'),
    url(r'^geojson/', LotsGeoJSON.as_view(), name='geojson'),
    url(r'^kml/', LotsKML.as_view(), name='kml'),
    url(r'^geojson-polygon/', LotsGeoJSONPolygon.as_view(),
        name='lot_geojson_polygon'),
    url(r'^geojson-centroid/', LotsGeoJSONCentroid.as_view(),
        name='lot_geojson_centroid'),
    url(r'^count/', LotsCountView.as_view(), name='lot_count'),
    url(r'^count-by-boundary/', LotsCountBoundaryView.as_view(),
        name='lot_count_by_boundary'),

    url(r'^(?P<pk>\d+)/$', LotDetailView.as_view(), name='lot_detail'),
    url(r'^(?P<pk>\d+)/geojson/$', LotGeoJSONDetailView.as_view(),
        name='lot_detail_geojson'),

    url(r'^(?P<pk>\d+)/grow-community/$',
        AddParticipantView.as_view(
            model=Organizer,
        ),
        name='add_organizer'),

    url(r'^(?P<lot_pk>\d+)/grow-community/(?P<hash>[^/]{30,})/(?P<pk>\d+)/success/$',
        AddParticipantSuccessView.as_view(
            model=Organizer,
        ),
        name='add_organizer_success'),

    url(r'^(?P<lot_pk>\d+)/grow-community/(?P<hash>[^/]{30,})/(?P<pk>\d+)/delete/$',
        DeletePhillyOrganizerView.as_view(),
        name='delete_organizer'),

    url(r'^organize/(?P<hash>[^/]{30,})/edit/$',
        EditLotParicipantView.as_view(),
        name='edit_participant'),

    url(r'^(?P<pk>\d+)/steward/add/$',
        AddStewardNotificationView.as_view(),
        name='add_stewardnotification'),

    url(r'^(?P<pk>\d+)/steward/add/success/$',
        AddStewardNotificationSuccessView.as_view(),
        name='add_stewardnotification_success'),

    url(r'^(?P<pk>\d+)/correction/add/$',
        AddGroundtruthRecordView.as_view(),
        name='add_groundtruthrecord'),

    url(r'^(?P<pk>\d+)/land-survey/$',
        EditLandCharacteristicsSurvey.as_view(),
        name='land_survey'),

    url(r'^(?P<pk>\d+)/photos/add/$',
        AddPhotoView.as_view(),
        name='add_photo'),

    url(r'^(?P<pk>\d+)/notes/add/$',
        AddNoteView.as_view(),
        name='add_note'),

    url(r'^(?P<pk>\d+)/files/add/$', AddFileView.as_view(), name='add_file'),
)
