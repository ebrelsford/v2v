from re import match

from pyproj import Proj, transform


METERS_PER_FOOT = 0.304800609601219

WGS84 = Proj(init='epsg:4326')

# the projection most Philly data is given in
PHILLY_PROJECTION = Proj('+proj=lcc +lat_1=39.93333333333333 '
                         '+lat_2=40.96666666666667 +lat_0=39.33333333333334 '
                         '+lon_0=-77.75 +x_0=600000 +y_0=0 +ellps=GRS80 '
                         '+towgs84=0,0,0,0,0,0,0 +units=m +no_defs')

ADDRESS_NUMBERED_STREET_REGEX = '^\s*(?:0*)(\d+\w+)\s*$'


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


def format_street_name(street_name):
    m = match(ADDRESS_NUMBERED_STREET_REGEX, street_name)
    if m:
        return m.group(1).lower()
    return street_name.title()


def fix_address(address):
    """Fix the formatting of an address for display."""
    if not address:
        return None
    components = address.split()

    # assume everything can be a street name
    components = [format_street_name(c) for c in components]
    return ' '.join(components)


def make_address(house_number=None, house_suffix=None, house_unit=None,
                 street_direction=None, street_name=None,
                 street_description=None, street_description_suffix=None):
    components = []

    if house_number:
        components.append(str(int(house_number)))
    if house_suffix:
        components.append(house_suffix)
    if house_unit:
        components.append(house_unit)
    if street_direction:
        components.append(street_direction.title())
    if street_name:
        components.append(format_street_name(street_name))
    if street_description:
        components.append(street_description.title())
    if street_description_suffix:
        components.append(street_description_suffix.title())
    components = [c.strip() for c in components if c]
    components = filter(lambda c: c and c != '', components)
    return ' '.join(components)
