"""
Python port of my java footprinting program
"""

import sys
import math
from pyproj import Proj
from pyproj import transform
from optparse import OptionParser


class Photo(object):
    data_fields = ['']
    photo_id = 0
    ground_height = 0
    x_value = 0
    y_value = 0
    z_value = 0
    # will need to convert o,p,k to radians
    o_value = 0
    p_value = 0
    k_value = 0
    rad_o_Value = 0
    rad_p_Value = 0
    rad_k_value = 0
    corner_coordinates = [[0, 0], [0, 0], [0, 0], [0, 0]]
    # rotation matrix elements
    r11 = 0
    r12 = 0
    r13 = 0
    r21 = 0
    r22 = 0
    r23 = 0
    r31 = 0
    r32 = 0
    r33 = 0
    epsg_code = 0
    # UCX image coordinates and focal length
    UCX_IMAGE_Y_FRONT = -33.912
    UCX_IMAGE_Y_BACK = 33.912
    UCX_IMAGE_X_RIGHT = -51.948
    UCX_IMAGE_X_LEFT = 51.948
    UCX_FOCAL_LENGTH = 100.5

    def __init__(self, next_line, ground_height, epsg_code):
        self.ground_height = ground_height
        self.epsg_code = epsg_code
        self.data_fields = next_line.split(',')
        self.photo_id = int(self.data_fields[0])
        self.x_value = float(self.data_fields[1])
        self.y_value = float(self.data_fields[2])
        self.z_value = float(self.data_fields[3])
        self.o_value = float(self.data_fields[4])
        self.p_value = float(self.data_fields[5])
        self.k_value = float(self.data_fields[6])
        self.rad_o_value = math.radians(self.o_value)
        self.rad_p_value = math.radians(self.p_value)
        self.rad_k_value = math.radians(self.k_value)
        self.compute_rotation_matrix()

    def compute_rotation_matrix(self):
        self.r11 = math.cos(self.rad_k_value) * math.cos(self.rad_p_value)
        self.r12 = math.cos(self.rad_k_value) * math.sin(self.rad_p_value) * math.sin(self.rad_o_value) - math.sin(self.rad_k_value) * math.cos(self.rad_o_value)
        self.r13 = math.cos(self.rad_k_value) * math.sin(self.rad_p_value) * math.cos(self.rad_o_value) + math.sin(self.rad_k_value) * math.sin(self.rad_o_value)
        self.r21 = math.sin(self.rad_k_value) * math.cos(self.rad_p_value)
        self.r22 = math.sin(self.rad_k_value) * math.sin(self.rad_p_value) * math.sin(self.rad_o_value) + math.cos(self.rad_k_value) * math.cos(self.rad_o_value)
        self.r23 = math.sin(self.rad_k_value) * math.sin(self.rad_p_value) * math.cos(self.rad_o_value) - math.cos(self.rad_k_value) * math.sin(self.rad_o_value)
        self.r31 = -math.sin(self.rad_p_value)
        self.r32 = math.cos(self.rad_p_value) * math.sin(self.rad_o_value)
        self.r33 = math.cos(self.rad_p_value) * math.cos(self.rad_o_value)

    def compute_corner_coordinates(self):
        # FrontRight X
        self.corner_coordinates[0][0] = self.x_value + (self.ground_height - self.z_value) \
            * ((self.r11 * self.UCX_IMAGE_X_RIGHT + self.r12 * self.UCX_IMAGE_Y_FRONT - self.r13 * self.UCX_FOCAL_LENGTH) /
               (self.r31 * self.UCX_IMAGE_X_RIGHT + self.r32 * self.UCX_IMAGE_Y_FRONT - self.r33 * self.UCX_FOCAL_LENGTH))

        # FrontRight Y
        self.corner_coordinates[0][1] = self.y_value + (self.ground_height - self.z_value) \
                * ((self.r21 * self.UCX_IMAGE_X_RIGHT + self.r22 * self.UCX_IMAGE_Y_FRONT - self.r23 * self.UCX_FOCAL_LENGTH) /
                   (self.r31 * self.UCX_IMAGE_X_RIGHT + self.r32 * self.UCX_IMAGE_Y_FRONT - self.r33 * self.UCX_FOCAL_LENGTH))

        # FrontLeft X
        self.corner_coordinates[1][0] = self.x_value + (self.ground_height - self.z_value) \
                * ((self.r11 * self.UCX_IMAGE_X_LEFT + self.r12 * self.UCX_IMAGE_Y_FRONT - self.r13 * self.UCX_FOCAL_LENGTH) /
                   (self.r31 * self.UCX_IMAGE_X_LEFT + self.r32 * self.UCX_IMAGE_Y_FRONT - self.r33 * self.UCX_FOCAL_LENGTH))

        # FrontLeft Y
        self.corner_coordinates[1][1] = self.y_value + (self.ground_height - self.z_value) \
                * ((self.r21 * self.UCX_IMAGE_X_LEFT + self.r22 * self.UCX_IMAGE_Y_FRONT - self.r23 * self.UCX_FOCAL_LENGTH) /
                   (self.r31 * self.UCX_IMAGE_X_LEFT + self.r32 * self.UCX_IMAGE_Y_FRONT - self.r33 * self.UCX_FOCAL_LENGTH))

        # BackRight X
        self.corner_coordinates[2][0] = self.x_value + (self.ground_height - self.z_value) \
                * ((self.r11 * self.UCX_IMAGE_X_RIGHT + self.r12 * self.UCX_IMAGE_Y_BACK - self.r13 * self.UCX_FOCAL_LENGTH) /
                   (self.r31 * self.UCX_IMAGE_X_RIGHT + self.r32 * self.UCX_IMAGE_Y_BACK - self.r33 * self.UCX_FOCAL_LENGTH))

        # BackRight Y
        self.corner_coordinates[2][1] = self.y_value + (self.ground_height - self.z_value) \
                * ((self.r21 * self.UCX_IMAGE_X_RIGHT + self.r22 * self.UCX_IMAGE_Y_BACK - self.r23 * self.UCX_FOCAL_LENGTH) /
                   (self.r31 * self.UCX_IMAGE_X_RIGHT + self.r32 * self.UCX_IMAGE_Y_BACK - self.r33 * self.UCX_FOCAL_LENGTH))

        # BackLeft X
        self.corner_coordinates[3][0] = self.x_value + (self.ground_height - self.z_value) \
                * ((self.r11 * self.UCX_IMAGE_X_LEFT + self.r12 * self.UCX_IMAGE_Y_BACK - self.r13 * self.UCX_FOCAL_LENGTH) /
                   (self.r31 * self.UCX_IMAGE_X_LEFT + self.r32 * self.UCX_IMAGE_Y_BACK - self.r33 * self.UCX_FOCAL_LENGTH))

        # BackLeft Y
        self.corner_coordinates[3][1] = self.y_value + (self.ground_height - self.z_value) \
                * ((self.r21 * self.UCX_IMAGE_X_LEFT + self.r22 * self.UCX_IMAGE_Y_BACK - self.r23 * self.UCX_FOCAL_LENGTH) /
                   (self.r31 * self.UCX_IMAGE_X_LEFT + self.r32 * self.UCX_IMAGE_Y_BACK - self.r33 * self.UCX_FOCAL_LENGTH))

        self.transform_to_lat_long()

    def transform_to_lat_long(self):
        user_projection = Proj(init='epsg:' + str(self.epsg_code))
        lat_long_projection = Proj(init='epsg:4326')

        for i in range(4):
            x1, y1 = (self.corner_coordinates[i][0], self.corner_coordinates[i][1])
            x2, y2 = transform(user_projection, lat_long_projection, x1, y1)
            self.corner_coordinates[i][0] = x2
            self.corner_coordinates[i][1] = y2

    def to_kml(self):
        # returns empty string if grouping separator is detected
        if self.data_fields[0] != "#":
            return  "    <Placemark>\n        <name>" + str(self.photo_id) + "</name>\n        <description>" \
                    + "xValue=" + str(self.x_value) \
                    + "\nyValue=" + str(self.y_value) \
                    + "\nzValue=" + str(self.z_value) \
                    + "\noValue=" + str(self.o_value) \
                    + "\npValue=" + str(self.p_value) \
                    + "\nkValue=" + str(self.k_value) \
                    + "\nGround Height=" + str(self.ground_height) \
                    + "\nCRS EPSG code=" + str(self.epsg_code) \
                    + "</description>\n" \
                    + "        <styleUrl>#msn_ylw-pushpin0</styleUrl>\n" \
                    + "        <Polygon>\n" \
                    + "            <tessellate>1</tessellate>\n" \
                    + "            <outerBoundaryIs>\n" \
                    + "                <LinearRing>\n" \
                    + "                    <coordinates>\n" \
                    + str(self.corner_coordinates[0][0]) + "," + str(self.corner_coordinates[0][1]) + "," + str(self.ground_height) + " " \
                    + str(self.corner_coordinates[1][0]) + "," + str(self.corner_coordinates[1][1]) + "," + str(self.ground_height) + " " \
                    + str(self.corner_coordinates[3][0]) + "," + str(self.corner_coordinates[3][1]) + "," + str(self.ground_height) + " " \
                    + str(self.corner_coordinates[2][0]) + "," + str(self.corner_coordinates[2][1]) + "," + str(self.ground_height) + "\n" \
                    + "                    </coordinates>\n" \
                    + "                </LinearRing>\n" \
                    + "            </outerBoundaryIs>\n" \
                    + "        </Polygon>\n    </Placemark>\n"


def main(file_name, ground_height, epsg_code):
    output = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + \
             "\n<kml xmlns=\"http://www.opengis.net/kml/2.2\"" + \
             " xmlns:gx=\"http://www.google.com/kml/ext/2.2\"" + \
             " xmlns:kml=\"http://www.opengis.net/kml/2.2\"" + \
             " xmlns:atom=\"http://www.w3.org/2005/Atom\">\n" + \
             "<Document>\n" + \
             "    <name>FOOTPRINTS</name>\n" + \
             "    <open>1</open>\n" + \
             "    <Style id=\"sh_ylw-pushpin\">\n" + \
             "        <IconStyle>\n" + \
             "            <scale>1.3</scale>\n" + \
             "            <Icon>\n"+ \
             "                <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n" + \
             "            </Icon>\n" + \
             "            <hotSpot x=\"20\" y=\"2\" xunits=\"pixels\" yunits=\"pixels\"/>\n" + \
             "        </IconStyle>\n" + \
             "        <LineStyle>\n" + \
             "            <color>87000000</color>\n" + \
             "            <width>1.9</width>\n" + \
             "        </LineStyle>\n" + \
             "        <PolyStyle>\n" + \
             "            <color>7300aa00</color>\n" + \
             "            <outline>0</outline>\n" + \
             "        </PolyStyle>\n" + \
             "    </Style>\n" + \
             "    <Style id=\"sn_ylw-pushpin\">\n" + \
             "        <IconStyle>\n" + \
             "            <scale>1.1</scale>\n" + \
             "            <Icon>\n" + \
             "                <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n" + \
             "            </Icon>\n" + \
             "            <hotSpot x=\"20\" y=\"2\" xunits=\"pixels\" yunits=\"pixels\"/>\n" + \
             "        </IconStyle>\n" + \
             "        <LineStyle>\n" + \
             "            <color>87000000</color>\n" + \
             "            <width>1.9</width>\n" + \
             "        </LineStyle>\n" + \
             "        <PolyStyle>\n" + \
             "            <color>7300aa00</color>\n" + \
             "            <outline>0</outline>\n" + \
             "        </PolyStyle>\n" + \
             "    </Style>\n" + \
             "    <StyleMap id=\"msn_ylw-pushpin0\">\n" + \
             "        <Pair>\n" + \
             "            <key>normal</key>\n" + \
             "            <styleUrl>#sn_ylw-pushpin</styleUrl>\n" + \
             "        </Pair>\n" + \
             "        <Pair>\n" + \
             "            <key>highlight</key>\n" + \
             "            <styleUrl>#sh_ylw-pushpin</styleUrl>\n" + \
             "        </Pair>\n" + \
             "    </StyleMap>)\n"

    with open(file_name) as f:
        input_lines = f.readlines()

    for line in input_lines:
        p = Photo(line, ground_height, epsg_code)
        p.compute_corner_coordinates()
        output += p.to_kml()

    output += "</Document>\n</kml>"
    print output


if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", type="string", dest="file_name",
                      default='sample_input.txt', help="input file")
    parser.add_option("-g", "--ground-height", type="int", dest="ground_height",
                      default=250, help="average ground height")
    parser.add_option("-c", "--epsg-code", type="int", dest="epsg_code",
                      default=2180, help="epsg code")
    (options, args) = parser.parse_args()
    sys.exit(main(options.file_name, options.ground_height, options.epsg_code))
