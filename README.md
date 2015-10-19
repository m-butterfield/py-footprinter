Footprinter
===========

[![Circle CI](https://circleci.com/gh/m-butterfield/py-footprinter.png?circle-token=c615ced31f0190dbb0405f67aa1ccb44b8f3c9cd)](https://circleci.com/gh/m-butterfield/mattbutterfield.com)

Create Google Earth KML files containing polygons representing image footprints when provided with photogrammetric exterior orientation parameters (the x, y, z, and omega phi kappa coordinates of an aerial camera at the moment a photo was taken), which can be provided in any coordinate system with an EPSG code.

## Example Usage

    $ ./footprinter sample_input.txt 90 2180 --output-file output.kml
