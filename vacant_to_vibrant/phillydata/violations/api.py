from phillydata.li.api import LIReader


class LIViolationReader(LIReader):

    endpoint = 'violationdetails'

    def get(self, code, since=None, params={}):
        filters = [ "violation_code eq '%s'" % code, ]
        if since:
            filters.append("violation_datetime gt %s" %
                           self.format_datetime(since))

        params.update({
            '$expand': 'locations',
            '$filter': ' and '.join(filters),
            'orderby': 'violation_datetime desc',
        })
        return super(LIViolationReader, self).get(self.endpoint, params)
