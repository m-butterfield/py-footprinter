"""
Python port of my java footprinting program
"""

import sys
import math
from optparse import OptionParser


class Photo(object):
    data_fields = []
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
    corner_coordinates = [[0, 0, 0, 0], [0, 0, 0, 0]]
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
        # detect grouping separator
        if "#" in next_line:
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
        else:
            self.data_fields[0] = "#"

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
        if self.data_fields[0] != "#":
            # FrontRight X
            self.corner_coordinates[0][0] = self.x_value + (self.ground_height - z_value) \
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

            self.transform_to_lat_long(self.corner_coordinates)

    def transform_to_lat_long(points):
        pass
        # TODO: figure this out for python...
        # Projection projection = ProjectionFactory.getNamedPROJ4CoordinateSystem(this.EPSGcode)
        # for (int i = 0 i < 4 i++) {
        #     Point2D.Double point = new Point2D.Double(points[i][0], points[i][1])
        #     projection.inverseTransform(point, point)
        #     points[i][0] = point.getX()
        #     points[i][1] = point.getY()

    def to_xml(self):
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

def main(file_name, epsg_code):
    p = Photo()
    print p.to_xml()

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", type="string", dest="file_name",
                      default='sample_input.txt', help="input file")
    parser.add_option("-c", "--epsg-code", type="int", dest="epsg_code",
                      default='2048', help="epsg code")
    (options, args) = parser.parse_args()
    sys.exit(main(options.file, options.epsg_code))
