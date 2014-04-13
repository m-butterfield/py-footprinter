"""
Python port of my java footprinting program
"""

import sys
from optparse import OptionParser


def main(file_name, epsg_code):
    pass

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", type="string", dest="file_name",
                      default='sample_input.txt', help="input file")
    parser.add_option("-c", "--epsg-code", type="int", dest="epsg_code",
                      default='2048', help="epsg code")
    (options, args) = parser.parse_args()
    sys.exit(main(options.file, options.epsg_code))
