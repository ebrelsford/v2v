from django.http import Http404, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from feincms.module.page.models import Page

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
    redirect_to_page_slug = 'pathways-list'

    def get(self, request, *args, **kwargs):
        try:
            page = Page.objects.get(slug__iexact=self.redirect_to_page_slug)
            return HttpResponseRedirect(page.get_absolute_url())
        except Exception:
            raise Http404
