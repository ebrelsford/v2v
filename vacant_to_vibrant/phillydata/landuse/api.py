from arcgisrest.reader import ArcGISRestServerReader


class LandUseReader(ArcGISRestServerReader):
    """Iterates over land use."""

    def __init__(self):
        super(LandUseReader, self).__init__(
            ('http://gis.phila.gov/ArcGIS/rest/services/'
             'PhilaOIT-GIS_Boundaries/MapServer/11/query?'),
            'esriGeometryEnvelope',
            '-8380165.3986,4846635.8111,-8344035.7458,4886006.8845',
            where=["C_DIG2DESC='Vacant'"],
        )
