import csv

from django.core.serializers import json
from django.http import HttpResponse
from django.views.generic import View


class JSONResponseView(View):
    response_class = HttpResponse

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        """Simple render to JSON"""
        return self.response_class(
            json.json.dumps(self.get_context_data(**self.kwargs),
                            cls=json.DjangoJSONEncoder, ensure_ascii=False),
            mimetype='application/json',
        )


class CSVView(View):
    response_class = HttpResponse

    def get(self, request, *args, **kwargs):
        return self.render_to_response()

    def get_fields(self):
        """Get the fields (column names) for this CSV"""
        raise NotImplementedError

    def get_filename(self):
        """Get the filename for this CSV"""
        return 'download'

    def get_rows(self):
        """
        Get the rows for this CSV

        The rows must be dicts of field (column) names to field values.

        """
        raise NotImplementedError

    def write_csv(self, response):
        fields = self.get_fields()
        csv_file = csv.DictWriter(response, fields)

        # Write header
        response.write(','.join(['%s' % field.replace('_', ' ') for field in fields]))
        response.write('\n')

        # Write rows
        for row in self.get_rows():
            csv_file.writerow(row)

    def render_to_response(self):
        """
        Simple render to CSV.
        """
        response = self.response_class(mimetype='text/csv')
        response['Content-Disposition'] = ('attachment; filename="%s.csv"' %
                                           self.get_filename())
        self.write_csv(response)
        return response
