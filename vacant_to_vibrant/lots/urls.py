from django.conf.urls.defaults import patterns, url

from inplace.views import PlacesDetailView
from recaptcha_works.decorators import fix_recaptcha_remote_ip

from organize.models import Organizer, Watcher
from .models import Lot
from .views import (EditLotParicipantView, AddParticipantView, LotsGeoJSON,
                    AddParticipantSuccessView, AddPhotoView,
                    AddNoteView, AddFileView, LotsCountView)


urlpatterns = patterns('',
    url(r'^geojson/', LotsGeoJSON.as_view()),
    url(r'^count/', LotsCountView.as_view()),

    url(r'^(?P<pk>\d+)/$',
        PlacesDetailView.as_view(
            model=Lot,
        ),
        name='lot_detail'),

    url(r'^(?P<pk>\d+)/organize/$',
        fix_recaptcha_remote_ip(AddParticipantView.as_view(
            model=Organizer,
        )),
        name='add_organizer'),

    url(r'^(?P<pk>\d+)/watch/$',
        fix_recaptcha_remote_ip(AddParticipantView.as_view(
            model=Watcher,
        )),
        name='add_watcher'),

    url(r'^(?P<pk>\d+)/organize/organizer/(?P<hash>[^/]{30,})/success/$',
        AddParticipantSuccessView.as_view(
            model=Organizer,
        ),
        name='add_organizer_success'),

    url(r'^(?P<pk>\d+)/organize/watcher/(?P<hash>[^/]{30,})/success/$',
        AddParticipantSuccessView.as_view(
            model=Watcher,
        ),
        name='add_watcher_success'),

    url(r'^organize/(?P<hash>[^/]{30,})/edit/$',
        EditLotParicipantView.as_view(),
        name='edit_participant'),

    url(r'^(?P<pk>\d+)/photos/add/$',
        fix_recaptcha_remote_ip(AddPhotoView.as_view()),
        name='add_photo'),

    url(r'^(?P<pk>\d+)/notes/add/$',
        fix_recaptcha_remote_ip(AddNoteView.as_view()),
        name='add_note'),

    url(r'^(?P<pk>\d+)/files/add/$',
        fix_recaptcha_remote_ip(AddFileView.as_view()),
        name='add_file'),
)
