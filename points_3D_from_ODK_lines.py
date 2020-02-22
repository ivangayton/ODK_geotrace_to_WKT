#!/bin/python3
"""
Takes a CSV file containing line strings from an OpenDataKit Geotrace, which
consist of a series of text coordinates, and returns a similar CSV file with 
3-dimensional points (lat, lon, and elevation columns).
"""
__version__ = '2020-02-20'

import os
import sys
import csv
import argparse

def main(infile, column = None, delimiter = ';',
         column_name = 'geotrace', output = None, keep_columns = None):
    """Iterates through a CSV containing a Javarosa (OpenDataKit) Geotrace
       and writes a new CSV with 3D points.
    """

    print('Input file: {}, column: {}, delimiter: {}, column name: {}, output: {}, keep columns: {}'.format(infile, column, delimiter, column_name, output, keep_columns))
    
    # Avoid choking the CSV library with a long linestring
    csv.field_size_limit(100000000)

    with open(infile) as line_data:
        of = output if output else '{}_{}.csv'.format(infile, '_3D_points')
        try:
            colindex = int(column) - 1 if column else header.index(column_name)
        except Exception as e:
            print('Maybe you have not specified a column number or name')
            print(e)
        reader = csv.reader(line_data, delimiter = delimiter)
        data = list(reader)
        original_header = data.pop(0)
        header = []
        if keep_columns:
            keepers = parse_column_numbers(keep_columns)
            header = [original_header[x - 1] for x in keepers]
        else:
            header = original_header[:colindex] + original_header[colindex + 1:]
        header.extend(['lat', 'lon', 'elevation', 'precision'])
        
        with open(of, 'w') as outfile:
            writer = csv.writer(outfile, delimiter = ';')
            writer.writerow(header)

            for row in data:
                try:
                    node_string = row[colindex]
                    nodes = node_string.split(';')
                    for node in nodes:
                        pointcoords = xyz_from_node(node)
                        if(pointcoords):
                            outrow = []
                            if(keep_columns):
                                keepers = parse_column_numbers(keep_columns)
                                outrow = [row[x - 1] for x in keepers]
                            else:
                                outrow = row[:colindex]
                                outrow.extend(row[colindex + 1:])
                            outrow.extend(pointcoords)
                            #import pdb;pdb.set_trace()
                            writer.writerow(outrow)
                except Exception as e:
                    print('Something went wrong with row {}'.format(row))
                    print(e)
                    
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
        print('something went wrong with node: {}'.format(node))
        print(e)
    
def parse_column_numbers(keep_columns):
    """Returns a list of numbers parsed from a user-supplied argument in the
       form of a series of ranges (dash-delimited) or single numbers, all
       comma delimited. For example, the input '1-3,5,8-10' will return the list
       [1,2,3,5,8,9,10]. Allows user to specify which items in a list to keep;
       in this case, the columns in a dataset.
    """
    groups = keep_columns.strip().split(',')
    keepers = []
    for group in groups:
        element = group.strip().split('-')
        if element:
            if len(element) == 1:
                keepers.append(int(element[0]))
            elif len(element) == 2:
                for num in range(int(element[0]), int(element[1]) + 1):
                    keepers.append(num)
            elif len(element) > 2:
                print('element {} too long'.format(element))
    return keepers
	       
if __name__ == "__main__":
    p = argparse.ArgumentParser()

    p.add_argument('infile', help = "Input CSV file")
    p.add_argument('-c', '--column', help =
                   'Column containing the linestrings to be converted to WKT'
                   '  with count starting from one.')
    p.add_argument('-cn', '--column_name', default = 'geotrace', help =
                   'The header name of the column containing the linestrings'
                   ' to be converted to WKT.')
    p.add_argument('-d', '--delimiter', default = ';', help =
                   'Token delimiting one value from the next. Usually , or ;')
    p.add_argument('-o', '--output', help = 'Output file path')
    p.add_argument('-kc', '--keep_columns', default = '', help =
                   'Specify the columns of the file containing the line trace'
                   ' you wish to keep in the point dataset.')
    
    args = p.parse_args()

    main(args.infile, args.column, args.delimiter,
         args.column_name, args.output, args.keep_columns)
