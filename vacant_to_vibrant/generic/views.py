from django.core.serializers import json
from django.http import HttpResponse
from django.views.generic import View


class JSONResponseView(View):
    response_class = HttpResponse

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        """
        Simple render to GeoJSON.
        """
        return self.response_class(
            json.json.dumps(self.get_context_data(**self.kwargs),
                            cls=json.DjangoJSONEncoder, ensure_ascii=False),
            mimetype='application/json',
        )
