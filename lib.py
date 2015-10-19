"""
Lib for footprinter project

"""
from collections import namedtuple
from math import cos, radians, sin

from jinja2 import Environment, FileSystemLoader

from pyproj import Proj, transform


DEFAULT_OUTPUT_FILE = 'output.kml'

LAT_LONG_EPSG = 'epsg:4326'
LAT_LONG_PROJ = Proj(init=LAT_LONG_EPSG)

UCX_IMAGE_Y_FRONT = -33.912
UCX_IMAGE_Y_BACK = 33.912
UCX_IMAGE_X_RIGHT = -51.948
UCX_IMAGE_X_LEFT = 51.948
UCX_FOCAL_LENGTH = 100.5


class InvalidEPSGCode(Exception):
    """
    Exception to raise when a Proj object cannot be created from an EPSG code

    """


class _Photo(namedtuple('Photo', [
    'id',
    'front_right',
    'front_left',
    'back_right',
    'back_left',
])):
    pass


class _Point(namedtuple('Point', ['x', 'y'])):
    pass


def create_footprints(input_file,
                      ground_height,
                      epsg_code,
                      output_file=DEFAULT_OUTPUT_FILE):
    """
    Create a Google Earth KML file containing polygons representing image
    footprints when provided with photogrammetric exterior orientation
    parameters (the x, y, z, and omega phi kappa coordinates of an aerial
    camera at the exact moment a photo was taken), which can be provided in any
    coordinate system.

    Args:
        input_file (str): Name of the input file
        ground_height (int): Average ground height of the area
        epsg_code (int): EPSG code of the input data

    Kwargs:
        output_file (str): Name of the output file

    """
    try:
        user_proj = Proj(init='epsg:{}'.format(epsg_code))
    except Exception:
        raise InvalidEPSGCode("Invalid EPSG code: {}".format(epsg_code))

    photos = []
    with open(input_file) as fp:
        for line in fp:
            photo_id, x, y, z, o, p, k = line.split(',')
            photos.append(_compute_footprint(photo_id,
                                             user_proj,
                                             ground_height,
                                             float(x),
                                             float(y),
                                             float(z),
                                             float(o),
                                             float(p),
                                             float(k)))

    _write_output_file(photos, ground_height, output_file)


def _compute_footprint(photo_id, user_proj, ground_height, x, y, z, o, p, k):
    r11, r12, r13, r21, r22, r23, r31, r32, r33 = _compute_matrix(o, p, k)
    return _compute_corner_coordinates(
        photo_id, user_proj, ground_height,
        r11, r12, r13, r21, r22, r23, r31, r32, r33, x, y, z)


def _compute_matrix(o, p, k):
    o_rad = radians(o)
    p_rad = radians(p)
    k_rad = radians(k)
    r11 = cos(k_rad) * cos(p_rad)
    r12 = cos(k_rad) * sin(p_rad) * sin(o_rad) - sin(k_rad) * cos(o_rad)
    r13 = cos(k_rad) * sin(p_rad) * cos(o_rad) + sin(k_rad) * sin(o_rad)
    r21 = sin(k_rad) * cos(p_rad)
    r22 = sin(k_rad) * sin(p_rad) * sin(o_rad) + cos(k_rad) * cos(o_rad)
    r23 = sin(k_rad) * sin(p_rad) * cos(o_rad) - cos(k_rad) * sin(o_rad)
    r31 = -sin(p_rad)
    r32 = cos(p_rad) * sin(o_rad)
    r33 = cos(p_rad) * cos(o_rad)
    return r11, r12, r13, r21, r22, r23, r31, r32, r33


def _compute_corner_coordinates(
        photo_id, user_proj, ground_height,
        r11, r12, r13, r21, r22, r23, r31, r32, r33, x, y, z):
    fr_x = (
        x + (ground_height - z) *
        ((r11 * UCX_IMAGE_X_RIGHT + r12 * UCX_IMAGE_Y_FRONT -
          r13 * UCX_FOCAL_LENGTH) /
         (r31 * UCX_IMAGE_X_RIGHT + r32 * UCX_IMAGE_Y_FRONT -
          r33 * UCX_FOCAL_LENGTH)))
    fr_y = (
        y + (ground_height - z) *
        ((r21 * UCX_IMAGE_X_RIGHT + r22 * UCX_IMAGE_Y_FRONT -
          r23 * UCX_FOCAL_LENGTH) /
         (r31 * UCX_IMAGE_X_RIGHT + r32 * UCX_IMAGE_Y_FRONT -
          r33 * UCX_FOCAL_LENGTH)))
    fl_x = (
        x + (ground_height - z) *
        ((r11 * UCX_IMAGE_X_LEFT + r12 * UCX_IMAGE_Y_FRONT -
          r13 * UCX_FOCAL_LENGTH) /
         (r31 * UCX_IMAGE_X_LEFT + r32 * UCX_IMAGE_Y_FRONT -
          r33 * UCX_FOCAL_LENGTH)))
    fl_y = (
        y + (ground_height - z) *
        ((r21 * UCX_IMAGE_X_LEFT + r22 * UCX_IMAGE_Y_FRONT -
          r23 * UCX_FOCAL_LENGTH) /
         (r31 * UCX_IMAGE_X_LEFT + r32 * UCX_IMAGE_Y_FRONT -
          r33 * UCX_FOCAL_LENGTH)))
    br_x = (
        x + (ground_height - z) *
        ((r11 * UCX_IMAGE_X_RIGHT + r12 * UCX_IMAGE_Y_BACK -
          r13 * UCX_FOCAL_LENGTH) /
         (r31 * UCX_IMAGE_X_RIGHT + r32 * UCX_IMAGE_Y_BACK -
          r33 * UCX_FOCAL_LENGTH)))
    br_y = (
        y + (ground_height - z) *
        ((r21 * UCX_IMAGE_X_RIGHT + r22 * UCX_IMAGE_Y_BACK -
          r23 * UCX_FOCAL_LENGTH) /
         (r31 * UCX_IMAGE_X_RIGHT + r32 * UCX_IMAGE_Y_BACK -
          r33 * UCX_FOCAL_LENGTH)))
    bl_x = (
        x + (ground_height - z) *
        ((r11 * UCX_IMAGE_X_LEFT + r12 * UCX_IMAGE_Y_BACK -
          r13 * UCX_FOCAL_LENGTH) /
         (r31 * UCX_IMAGE_X_LEFT + r32 * UCX_IMAGE_Y_BACK -
          r33 * UCX_FOCAL_LENGTH)))
    bl_y = (
        y + (ground_height - z) *
        ((r21 * UCX_IMAGE_X_LEFT + r22 * UCX_IMAGE_Y_BACK -
          r23 * UCX_FOCAL_LENGTH) /
         (r31 * UCX_IMAGE_X_LEFT + r32 * UCX_IMAGE_Y_BACK -
          r33 * UCX_FOCAL_LENGTH)))

    return _Photo(
        id=photo_id,
        front_right=_Point(*transform(user_proj, LAT_LONG_PROJ, fr_x, fr_y)),
        front_left=_Point(*transform(user_proj, LAT_LONG_PROJ, fl_x, fl_y)),
        back_right=_Point(*transform(user_proj, LAT_LONG_PROJ, br_x, br_y)),
        back_left=_Point(*transform(user_proj, LAT_LONG_PROJ, bl_x, bl_y)))


def _write_output_file(photos, ground_height, output_file):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('output_tmpl.kml')
    t = template.render(photos=photos, ground_height=ground_height)
    with open(output_file or 'output.kml', 'wb') as f:
        f.write(t)
