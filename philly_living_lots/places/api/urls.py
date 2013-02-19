from django.conf.urls.defaults import include, patterns

from places.api import BuildingResource

building_resource = BuildingResource()

urlpatterns = patterns('',
    # TODO for app/model...
    (r'^pops/', include(building_resource.urls)),
)
