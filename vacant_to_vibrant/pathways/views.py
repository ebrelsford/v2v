from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Pathway


class PathwaysFeinCMSMixin(object):

    def render_to_response(self, context, **response_kwargs):
        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            return self.get_template_names(), context

        return super(PathwaysFeinCMSMixin, self).render_to_response(
            context, **response_kwargs)


class PathwaysDetailView(PathwaysFeinCMSMixin, DetailView):
    model = Pathway


class PathwaysListView(PathwaysFeinCMSMixin, ListView):
    #model = Pathway
    queryset = Pathway.objects.all()
