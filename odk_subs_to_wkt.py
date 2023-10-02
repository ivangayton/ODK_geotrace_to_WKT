#!/bin/python3
"""
Converts OpenDataKit (ODK) JavaRosa geometry in CSV to Well-Known Text (WKT).

Takes a CSV file containing line strings from an ODK submission, and 
returns a similar CSV file with properly formatted Well-Known Text (WKT) 
polygons, lines, and points.

The output file should be identical to the input, with the exception
of having converted the GeoTrace coordinates to valid WKT lines.

Arguments

Typical usage example:
           
    ./odk_subs_to_wkt.py /path/to/infile -c 9

    ./odk_subs_to_wkt.py /path/to/infile -cn i -d ';'
"""
__version__ = '2023-09-30'

import os
import sys
import csv
import argparse

def main(infile, column, column_name, delim, output):
    """
    Args:
        infile: filepath, a CSV from an ODK submission
        column: int, one-based column containing the 
        delim: str, CSV delimiter
        column_name: str, spreadsheet-style column name ex "AC"
        output: filepath, output CSV to write (if None autogenerates)
    Returns:
        None
        Side effect: Writes a CSV with additional columns of WKT
    """

    # Avoid choking the Python CSV library with a long linestring
    csv.field_size_limit(100000000)

    with open(infile) as line_data:
        reader = csv.reader(line_data, delimiter = delim)
        data = list(reader)
        of = output if output else f'{infile}_results.csv'
        with open(of, 'w') as outfile:
            writer = csv.writer(outfile, delimiter = delim)
            header = data.pop(0)
            colindex = int(column) - 1 if column else header.index(column_name)
            
            newheader = header
            newheader.append('WKT')
            writer.writerow(newheader)

            for row in data:
                node_string = row[colindex]
                outrow = row
                wktstring = wkt_from_jrstring(node_string)
                outrow.append(wktstring)
                writer.writerow(outrow)
        print('created output file at: \n{}\n'.format(of))
        
def wkt_from_jrstring(jrstring):
    """
    Args:
        str: arbitrarily long strings separated by semicolons 
        where the first two items in the string are expected 
        to be lat and lon (JavaRosa)
    Returns:
        str: those coordinates as a Well-Known Text
        (with lon first and lat second, therefore x,y).
    """ 
    nodes = jrstring.split(';')
    WKT_type = ''
    if len(nodes) < 1:
        WKT_type = 'POINT'
    else:
        if nodes[0] == nodes[-1]:
            WKT_type = "POLYGON"
        else: WKT_type = "LINESTRING"
    #print(f'\nnodes: {nodes}')
    firstnode = nodes.pop(0).strip().split()
    #print(f'\nfirst node is a {type(firstnode)}: {firstnode}')
    nodestring = f'POLYGON(({firstnode[1]} {firstnode[0]}'
    #print(f'Nodestring so far is: {nodestring}')
    for node in nodes:
        coords = node.strip().split()
        nodestring += f',{coords[1]} {coords[0]}'
    nodestring += '))'
    return nodestring

if __name__ == "__main__":

    arguments = []
    p = argparse.ArgumentParser()

    p.add_argument('infile', help = "Input CSV file")
    p.add_argument('-c', '--column', help =
                   'Column containing the linestrings to be converted to WKT')
    p.add_argument('-cn', '--column_name', default = 'geotrace', help =
                   'The header of the column containing the linestrings'
                   ' to be converted to WKT')
    p.add_argument('-d', '--delimiter', default = ',', help =
                   'Token delimiting one value from the next, usually , or ;')
    p.add_argument('-o', '--output', help = 'Output file path')
    a = p.parse_args()

    main(a.infile, a.column, a.column_name, a.delimiter, a.output)
