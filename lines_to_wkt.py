#!/bin/python3
"""
Takes a CSV file containing line strings from an OpenDataKit Geotrace, which
consist of a series of text coordinates, and returns a similar CSV file with 
properly formatted Well-Known Text (WKT) linestrings (and points).

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
__version__ = '2019-04-29'

import os
import sys
import csv
import argparse

def main(infile, column = None, delimiter = ';',
         column_name = 'drain_line', output = None):
    """Iterates through a CSV and writes a CSV with converted linestrings."""

    # Avoid choking the CSV library with a long linestring
    csv.field_size_limit(100000000)

    print(delimiter)

    with open(infile) as line_data:
        reader = csv.reader(line_data, delimiter = ';')
        data = list(reader)
        of = output if output else '{}_{}.csv'.format(infile, '_results')
        with open(of, 'w') as outfile:
            writer = csv.writer(outfile, delimiter = delimiter)
            header = data.pop(0)
            #add the elevation and precision to header
            header += ['elevation', 'precision']
            print(header)
            print(len(header))
            colindex = int(column) - 1 if column else header.index(column_name)
            writer.writerow(header)

            for row in data:
                print(len(row))
                #try:
                #print(row)
                #import pdb;pdb.set_trace()
                node_string = ''.join(row[colindex])
                outrow = row
                # linestring, elevation, precision = WKT_linestring_from_nodes(node_string)
                lon, lat, elev, precision = xyz_from_nodes(node_string)
                outrow[colindex] = linestring
                outrow.append(elevation)
                outrow.append(precision)
                writer.writerow(outrow)
                #except:
                #print('Cannot parse this line')
        print('created output file at: \n{}\n'.format(of))
        
def WKT_linestring_from_nodes(node_string):
    """Takes a string of arbitrarily long strings separated by semicolons 
    where the first two items in the string are expected to be lat and long.
    Returns a string containing those coordinates as a Well-Known Text
    linestring (with long first and lat second, therefore x,y).
    """
    nodes = node_string.split(';')
    if nodes:
        WKT_type = "LINESTRING" if len(nodes) > 1 else "POINT"
        coord_pair_list = []
        elevation = []
        precision = []
        for node in nodes:
            coords = node.strip().split()
            if(len(coords) >=2):   # can be >2 incl elev & precision values
                # Reverse coords; Lon first, then Lat (as per WKT spec)
                coord_pair = '{} {}'.format(coords[1], coords[0])
                coord_pair_list.append(coord_pair)
                elevation.append(coords[2])
                precision.append(coords[3])
        line_coord_string = ', '.join(coord_pair_list)
        linestring = '{}({})'.format(WKT_type, line_coord_string)
        return linestring, elevation, precision
    else:
        return None

def xyz_from_nodes(node_string):
    nodes = node_string.split(';')
    if nodes:
        lon = []
        lat = []
        elev = []
        precision = []
	for node in nodes:
        coords = node.strip().split()
        lon.append(coords[1])
        lat.append(coords[0])
        elev.append(coords[2])
        precision.append(coords[3])
    return lon, lat, elev, precision


	       
if __name__ == "__main__":

    arguments = []
    p = argparse.ArgumentParser()

    p.add_argument('infile', help = "Input CSV file")
    p.add_argument('-c', '--column', help =
                   'Column containing the linestrings to be converted to WKT')
    p.add_argument('-cn', '--column_name', default = 'drain_line', help =
                   'The header of the column containing the linestrings'
                   ' to be converted to WKT')
    p.add_argument('-d', '--delimiter', default = ',', help =
                   'Token delimiting one value from the next, usually , or ;')
    p.add_argument('-o', '--output', help = 'Output file path')
    args = p.parse_args()

    main(args.infile, args.column, args.delimiter,
         args.column_name, args.output)
