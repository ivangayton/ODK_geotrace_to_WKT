#!/bin/python3
"""
Takes a CSV file containing line strings from an OpenDataKit Geotrace, which
consist of a series of text coordinates, and returns a similar CSV file with 
properly formatted Well-Known Text (WKT) linestrings (and points).

Arguments:

  1) An input CSV file
  2) An integer specifying which column contains the geotrace 
     (1-based column count). 

Example usage:
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
"""
__version__ = '2017-08-15'

import os
import sys
import csv

def main(infile, geometry_column):
    outfile = create_outfile(infile, "_results.csv")
    csv.field_size_limit(100000000)  # Avoid problems with long linestrings

    with open(infile) as line_data:
        linereader = csv.reader(line_data, delimiter = ';')
        with open(outfile, 'w') as out_file:
            # Write the original CSV header directly to the outfile
            writer = csv.writer(out_file, delimiter = ',')
            header = next(linereader)
            writer.writerow(header)

            # Extract the line string from the appropriate column
            rownum = 1
            for row in linereader:
                #print(rownum)
                #print(row[31])
                rownum += 1
                geometry_col = int(geometry_column)-1
                node_string = ''.join(row[geometry_col])
                outrow = row
                outrow[geometry_col] = WKT_linestring_from_nodes(node_string)
                writer.writerow(outrow)
        print("created output file at:")
        print(outfile)
        

def WKT_linestring_from_nodes(node_string):
    """Takes a string of arbitrarily long strings separated by semicolons 
    where the first two items in the string are expected to be lat and long.
    Returns a string containing those coordinates as a Well-Known Text
    linestring (with long and lat in that order, therefore x,y).
    """
    nodes = node_string.split(';')
    # Return None if the input contains no nodes
    if (len(nodes) <= 1):
        return None

    WKT_type = "LINESTRING"
    if (len(nodes) == 2):
        WKT_type = "POINT"

    # Create the WKT string with WKT type and lon, lat in order
    coord_pair_list = []
    for node in nodes:
        # strip leading space from nodes string (some phones do this)
        if node.startswith(" "): node = node[1:]
        coords = node.split(' ')
        if(len(coords) >=2):
            coord_pair = coords[1] + ' ' + coords[0] + ', '
            coord_pair_list.append(coord_pair)
    line_coord_string = ''.join(coord_pair_list)
    linestring = WKT_type + '(' + line_coord_string + ')'
    return linestring

def create_outfile(infile, extension):
    try:
        infile_name = infile.split('.')[0]
        infile_extension = infile.split('.')[-1]
    except:
        print("check input file")
        sys.exit()
    outfile = infile_name + extension
    return outfile

if __name__ == "__main__":
    
    main( sys.argv[1], sys.argv[2])
