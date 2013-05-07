from phillydata.li.api import LIReader


class LILicenseReader(LIReader):
    endpoint = 'licenses'

    codes = ['3219', '3634',]

    def get(self, code, since=None, params={}):
        filters = [ "license_type_code eq '%s'" % code, ]
        if since:
            filters.append("issued_datetime gt %s" %
                           self.format_datetime(since))

        params.update({
            '$expand': 'locations',
            '$filter': ' and '.join(filters),
            'orderby': 'issued_datetime desc',
        })
        return super(LILicenseReader, self).get(self.endpoint, params)

