from django.conf.urls.defaults import patterns, url

from .views import MailParticipantsView

urlpatterns = patterns('',
    url(r'^$', MailParticipantsView.as_view()),
    url(r'^participants/mail/$', MailParticipantsView.as_view(),
        name="mail_participants"),
)
