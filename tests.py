"""
Footprinter tests

"""
import os
import unittest

from lib import create_footprints, InvalidEPSGCode


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
        create_footprints(
            INPUT_FILE_NAME, GROUND_HEIGHT, EPSG_CODE, OUTPUT_FILE_NAME)
        with open(OUTPUT_FILE_NAME) as fp:
            output = fp.read()
        self.assertEqual(self.expected_output, output)

    def test_invalid_epsg_code(self):
        self.assertRaises(InvalidEPSGCode,
                          create_footprints,
                          INPUT_FILE_NAME,
                          GROUND_HEIGHT,
                          'asdflkj',
                          OUTPUT_FILE_NAME)
