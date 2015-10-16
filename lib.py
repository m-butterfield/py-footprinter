"""
Lib for footprinter project

"""
import math

from pyproj import Proj, transform


UCX_IMAGE_Y_FRONT = -33.912
UCX_IMAGE_Y_BACK = 33.912
UCX_IMAGE_X_RIGHT = -51.948
UCX_IMAGE_X_LEFT = 51.948
UCX_FOCAL_LENGTH = 100.5


class Photo(object):

    def __init__(self, next_line, ground_height, epsg_code):
        self.ground_height = ground_height
        self.epsg_code = epsg_code
        self.r11 = None
        self.r12 = None
        self.r13 = None
        self.r21 = None
        self.r22 = None
        self.r23 = None
        self.r31 = None
        self.r32 = None
        self.r33 = None
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
        self.corner_coordinates = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.compute_rotation_matrix()

    def compute_rotation_matrix(self):
        self.r11 = math.cos(self.rad_k_value) * math.cos(self.rad_p_value)
        self.r12 = (math.cos(self.rad_k_value) * math.sin(self.rad_p_value) *
                    math.sin(self.rad_o_value) - math.sin(self.rad_k_value) *
                    math.cos(self.rad_o_value))
        self.r13 = (math.cos(self.rad_k_value) * math.sin(self.rad_p_value) *
                    math.cos(self.rad_o_value) + math.sin(self.rad_k_value) *
                    math.sin(self.rad_o_value))
        self.r21 = math.sin(self.rad_k_value) * math.cos(self.rad_p_value)
        self.r22 = (math.sin(self.rad_k_value) * math.sin(self.rad_p_value) *
                    math.sin(self.rad_o_value) + math.cos(self.rad_k_value) *
                    math.cos(self.rad_o_value))
        self.r23 = (math.sin(self.rad_k_value) * math.sin(self.rad_p_value) *
                    math.cos(self.rad_o_value) - math.cos(self.rad_k_value) *
                    math.sin(self.rad_o_value))
        self.r31 = -math.sin(self.rad_p_value)
        self.r32 = math.cos(self.rad_p_value) * math.sin(self.rad_o_value)
        self.r33 = math.cos(self.rad_p_value) * math.cos(self.rad_o_value)

    def compute_corner_coordinates(self):
        # FrontRight X
        self.corner_coordinates[0][0] = (
            self.x_value + (self.ground_height - self.z_value) *
            ((self.r11 * UCX_IMAGE_X_RIGHT + self.r12 * UCX_IMAGE_Y_FRONT -
              self.r13 * UCX_FOCAL_LENGTH) /
             (self.r31 * UCX_IMAGE_X_RIGHT + self.r32 * UCX_IMAGE_Y_FRONT -
              self.r33 * UCX_FOCAL_LENGTH)))

        # FrontRight Y
        self.corner_coordinates[0][1] = (
            self.y_value + (self.ground_height - self.z_value) *
            ((self.r21 * UCX_IMAGE_X_RIGHT + self.r22 * UCX_IMAGE_Y_FRONT -
              self.r23 * UCX_FOCAL_LENGTH) /
             (self.r31 * UCX_IMAGE_X_RIGHT + self.r32 * UCX_IMAGE_Y_FRONT -
              self.r33 * UCX_FOCAL_LENGTH)))

        # FrontLeft X
        self.corner_coordinates[1][0] = (
            self.x_value + (self.ground_height - self.z_value) *
            ((self.r11 * UCX_IMAGE_X_LEFT + self.r12 * UCX_IMAGE_Y_FRONT -
              self.r13 * UCX_FOCAL_LENGTH) /
             (self.r31 * UCX_IMAGE_X_LEFT + self.r32 * UCX_IMAGE_Y_FRONT -
              self.r33 * UCX_FOCAL_LENGTH)))

        # FrontLeft Y
        self.corner_coordinates[1][1] = (
            self.y_value + (self.ground_height - self.z_value) *
            ((self.r21 * UCX_IMAGE_X_LEFT + self.r22 * UCX_IMAGE_Y_FRONT -
              self.r23 * UCX_FOCAL_LENGTH) /
             (self.r31 * UCX_IMAGE_X_LEFT + self.r32 * UCX_IMAGE_Y_FRONT -
              self.r33 * UCX_FOCAL_LENGTH)))

        # BackRight X
        self.corner_coordinates[2][0] = (
            self.x_value + (self.ground_height - self.z_value) *
            ((self.r11 * UCX_IMAGE_X_RIGHT + self.r12 * UCX_IMAGE_Y_BACK -
              self.r13 * UCX_FOCAL_LENGTH) /
             (self.r31 * UCX_IMAGE_X_RIGHT + self.r32 * UCX_IMAGE_Y_BACK -
              self.r33 * UCX_FOCAL_LENGTH)))

        # BackRight Y
        self.corner_coordinates[2][1] = (
            self.y_value + (self.ground_height - self.z_value) *
            ((self.r21 * UCX_IMAGE_X_RIGHT + self.r22 * UCX_IMAGE_Y_BACK -
              self.r23 * UCX_FOCAL_LENGTH) /
             (self.r31 * UCX_IMAGE_X_RIGHT + self.r32 * UCX_IMAGE_Y_BACK -
              self.r33 * UCX_FOCAL_LENGTH)))

        # BackLeft X
        self.corner_coordinates[3][0] = (
            self.x_value + (self.ground_height - self.z_value) *
            ((self.r11 * UCX_IMAGE_X_LEFT + self.r12 * UCX_IMAGE_Y_BACK -
              self.r13 * UCX_FOCAL_LENGTH) /
             (self.r31 * UCX_IMAGE_X_LEFT + self.r32 * UCX_IMAGE_Y_BACK -
              self.r33 * UCX_FOCAL_LENGTH)))

        # BackLeft Y
        self.corner_coordinates[3][1] = (
            self.y_value + (self.ground_height - self.z_value) *
            ((self.r21 * UCX_IMAGE_X_LEFT + self.r22 * UCX_IMAGE_Y_BACK -
              self.r23 * UCX_FOCAL_LENGTH) /
             (self.r31 * UCX_IMAGE_X_LEFT + self.r32 * UCX_IMAGE_Y_BACK -
              self.r33 * UCX_FOCAL_LENGTH)))

        self.transform_to_lat_long()

    def transform_to_lat_long(self):
        user_projection = Proj(init='epsg:' + str(self.epsg_code))
        lat_long_projection = Proj(init='epsg:4326')

        for i in range(4):
            x1 = self.corner_coordinates[i][0]
            y1 = self.corner_coordinates[i][1]
            x2, y2 = transform(user_projection, lat_long_projection, x1, y1)
            self.corner_coordinates[i][0] = x2
            self.corner_coordinates[i][1] = y2