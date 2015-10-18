"""
Footprinter tests

"""
import os
import unittest

from jinja2 import Environment, FileSystemLoader

from lib import Photo


INPUT_FILE_NAME = 'sample_input.txt'
OUTPUT_FIXTURE_FILE_NAME = 'sample_output.kml'
OUTPUT_FILE_NAME = 'test_output.kml'
GROUND_HEIGHT = 90
EPSG_CODE = 2180


class FootprinterTest(unittest.TestCase):

    def setUp(self):
        with open(INPUT_FILE_NAME) as fp:
            self.input_lines = fp.readlines()
        with open(OUTPUT_FIXTURE_FILE_NAME) as fp:
            self.expected_output = fp.read()

    def tearDown(self):
        try:
            os.remove(OUTPUT_FILE_NAME)
        except OSError:
            pass

    def test_footprinter(self):
        footprints = []
        for line in self.input_lines:
            p = Photo(line, GROUND_HEIGHT, EPSG_CODE)
            p.compute_corner_coordinates()
            footprints.append(p)
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('output_tmpl.kml')
        t = template.render(footprints=footprints)
        with open(OUTPUT_FILE_NAME, 'wb') as fp:
            fp.write(t)
        with open(OUTPUT_FILE_NAME) as fp:
            output = fp.read()
        self.assertEqual(self.expected_output, output)
