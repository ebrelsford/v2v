from pyproj import Proj, transform


METERS_PER_FOOT = 0.304800609601219

WGS84 = Proj(init='epsg:4326')

# the projection most Philly data is given in
PHILLY_PROJECTION = Proj('+proj=lcc +lat_1=39.93333333333333 '
                         '+lat_2=40.96666666666667 +lat_0=39.33333333333334 '
                         '+lon_0=-77.75 +x_0=600000 +y_0=0 +ellps=GRS80 '
                         '+towgs84=0,0,0,0,0,0,0 +units=m +no_defs')


def to_lon_lat(x, y):
    # convert to meters
    (x, y) = [coord * METERS_PER_FOOT for coord in (x, y)]

    # reproject
    return transform(PHILLY_PROJECTION, WGS84, x, y)


def to_point(lon, lat):
    # reproject
    x, y = PHILLY_PROJECTION(lon, lat)

    # convert to feet
    return [coord / METERS_PER_FOOT for coord in (x, y)]
