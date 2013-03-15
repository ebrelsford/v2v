from django.conf.urls import patterns, url
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from pathways.models import Pathway


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        queryset=Pathway.objects.all(),
    ), name='pathway_list'),

    url(r'^(?P<slug>[^/]+)/$', DetailView.as_view(
        queryset=Pathway.objects.all(),
    ), name='pathway_detail'),
)
