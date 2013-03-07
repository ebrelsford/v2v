from arcgisrest.reader import ArcGISRestServerReader


class AvailablePropertyReader(ArcGISRestServerReader):
    """
    Iterates over available properties listed here:
        http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/0/

    """
    def __init__(self):
        super(AvailablePropertyReader, self).__init__(
            'http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/0/query?',
            'esriGeometryEnvelope',
            '-1.00006902217865,-1.00007303059101,2745294.56838398,300739.423707381'
        )
