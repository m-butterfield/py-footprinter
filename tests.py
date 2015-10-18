"""
Footprinter tests

"""
import unittest

from jinja2 import Environment, FileSystemLoader

from lib import Photo


INPUT_FILE_NAME = 'sample_input.txt'
OUTPUT_FILE_NAME = 'sample_output.kml'
GROUND_HEIGHT = 90
EPSG_CODE = 2180


class FootprinterTest(unittest.TestCase):

    def setUp(self):
        with open(INPUT_FILE_NAME) as fp:
            self.input_lines = fp.readlines()
        with open(OUTPUT_FILE_NAME) as fp:
            self.expected_output = fp.read()

    def test_footprinter(self):
        footprints = []
        for line in self.input_lines:
            p = Photo(line, GROUND_HEIGHT, EPSG_CODE)
            p.compute_corner_coordinates()
            footprints.append(p)
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('output_tmpl.kml')
        t = template.render(footprints=footprints)
        self.assertEqual(self.expected_output, t)
