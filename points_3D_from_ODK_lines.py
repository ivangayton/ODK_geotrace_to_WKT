#!/bin/python3
"""
Takes a CSV file containing line strings from an OpenDataKit Geotrace, which
consist of a series of text coordinates, and returns a similar CSV file with 
3-dimensional points (lat, lon, and elevation columns).

This script expects the default GeoTrace format from an ODK CSV export from
Kobo Toolbox, which consists of a series of node coordinates separated by 
semicolons. Each node seems to consist of a latitude, longitude, and two zeros, 
internally separated by spaces. 

The output file should be identical to the input, with the exception
of having converted the GeoTrace coordinates to valid WKT lines.
"""
__version__ = '2019-04-29'

import os
import sys
import csv
import argparse

def main(infile, column = None, delimiter = ';',
         column_name = 'drain_line', output = None):
    print(column)
    """Iterates through a CSV and writes a CSV with 3D points."""

    # Avoid choking the CSV library with a long linestring
    csv.field_size_limit(100000000)

    print(delimiter)

    with open(infile) as line_data:
        reader = csv.reader(line_data, delimiter = ';')
        data = list(reader)
        of = output if output else '{}_{}.csv'.format(infile, '_3D_points')
        colindex = int(column) - 1 if column else header.index(column_name)
        with open(of, 'w') as outfile:
            writer = csv.writer(outfile, delimiter = ';')
            header = data.pop(0)
            newheader = header[:colindex]
            newheader.extend(header[colindex + 1:])
            newheader.extend(['lat', 'lon', 'elevation', 'precision'])

            writer.writerow(newheader)

            for row in data:
                node_string = row[colindex]
                nodes = node_string.split(';')
                for node in nodes:
                    pointcoords = xyz_from_node(node)
                    if(pointcoords):
                        outrow = row[:colindex]
                        outrow.extend(row[colindex + 1:])
                        outrow.extend(pointcoords)
                        #import pdb;pdb.set_trace()
                        writer.writerow(outrow)
        
        print('created output file at: \n{}\n'.format(of))
        
def xyz_from_node(node):
    try:
        if node:
            coords = node.strip().split()
            lat = coords[0]
            lon = coords[1]
            elev = coords[2]
            precision = coords[3]
            returnlist = [lat, lon, elev, precision]
            return coords
    except Exception as e:
        print('something went wrong with this node')
        print(e)
    

	       
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
