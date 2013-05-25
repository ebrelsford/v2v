from django.conf.urls.defaults import patterns, url

from .views import (MailParticipantsView, MailParticipantsCountView,
                    MailParticipantsSuccessView)

urlpatterns = patterns('',
    url(r'^participants/mail/$', MailParticipantsView.as_view(),
        name='mail_participants'),
    url(r'^participants/count/$', MailParticipantsCountView.as_view(),
        name='mail_participants_count'),
    url(r'^participants/success/$', MailParticipantsSuccessView.as_view(),
        name='mail_participants_success'),
)
