# Utility to convert ODK Geotraces to Well-Known Text linestrings

Takes a CSV file containing line strings from an OpenDataKit Geotrace, which
consist of a series of text coordinates, and returns a similar CSV file with 
properly formatted Well-Known Text (WKT) linestrings (and points).

**Arguments:**

  1) An input CSV file
  2) An integer specifying which column contains the geotrace 
     (1-based column count). 

**Example usage:**

    python3 lines_to_wkt.py infile.csv 9 outfile.csv

where the ninth column in the input file is the GeoTrace.

This script expects the default GeoTrace format from an ODK CSV export from
Kobo Toolbox, which consists of a series of node coordinates separated by 
semicolons. Each node seems to consist of a latitude, longitude, and two zeros, 
internally separated by spaces. The WKT format specifies the type 
(LINESTRING or POINT) followed by long, then lat separated by spaces, 
then a comma separating nodes.

The output file should be identical to the input, with the exception
of having converted the GeoTrace coordinates to valid WKT lines.

In a future version I may allow additional column number arguments to convert 
multiple traces in the same file (in case someone collects multiple lines in 
the same survey).