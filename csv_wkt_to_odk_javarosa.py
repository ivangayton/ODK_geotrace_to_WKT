#!/bin/python3
"""
Converts CSV with Well-Known Text (WKT) geometry to CSV with OpenDataKit 
(ODK) compatible JavaRosa geometry.

Takes a CSV file from QGIS or other with properly formatted Well-Known Text (WKT) polygons, lines, and points in a 'WKT' column (which is how you'll get it from something like QGIS), and returns a similar CSV file with JavaRosa-style strings representing the geometry.

JavaRosa geometry consists of:
  - Nodes (points) which are space-separated strings of four numbers
    - y (lat) in degrees
    - x (lon) in degrees
    - elevation in meters above sea level (I mean, not really but close enough)
    - Accuracy (approximate margin of error in meters, not very statistically rigorous)

Theoretically this could be in any Coordinate Reference System, but in practice it's always WGS84 unprojected lat/lon (EPSG:4326). The upshot of this is that you don't have to worry about CRS or projections.

The output file should be identical to the input, with the exception
of having converted the geometry to JavaRosa format.

Positional arguments
- Input CSV file

Flag arguments
- Optional: -c --column: Geometry column number (1-based) 
  OR 
  -cn --column_name: spreadsheet-style (A-ZZ) column ID. 
If you don't provide this it just looks for a column with header 'geometry'
- Optional: Delimiter to use for CSV creation. If you don't specify this it uses commas.
- Optional: Output file. If you don't specify this it tacks '_results.csv' onto the input filename and saves it as that.


Typical usage example:
           
    ./csv_wkt_to_odk_javarosa.py /path/to/infile -c 9

    ./csv_wkt_to_odk_javarosa.py /path/to/infile -cn i -d ';'
"""
__version__ = '2024-03-18'

import os
import sys
import csv
import argparse

def convert_to_javarosa(infile, column, column_name, delim, output):
    """Converts an entire CSV file to one usable in ODK as an Entity list
    by creating a 'geometry' column containing a JavaRosa representation
    of the Well-Known Text geometry from most GIS-ish systems.
    Args:
        infile: filepath, a CSV with Well-Known-Text geometry in it
        column: int, one-based column containing the 
        delim: str, CSV delimiter
        column_name: str, spreadsheet-style column name ex "AC"
        output: filepath, output CSV to write (if None autogenerates)
    Returns:
        None
        Side effect: Writes a CSV with WKT geometry replaced by JavaRosa
    """
    # Avoid choking the Python CSV library with a long linestring
    csv.field_size_limit(100000000)

    with open(infile) as line_data:
        reader = csv.reader(line_data, delimiter = delim)
        data = list(reader)

        # If the user specified an output filepath, use it. Otherwise
        # just append _results.csv to the input filepath and use that.
        of = output if output else f'{infile}_results.csv'
        with open(of, 'w') as outfile:
            writer = csv.writer(outfile, delimiter = delim)
            header = data.pop(0)
            colindex = int(column) - 1 if column else header.index(column_name)

            newheader = header
            # TODO: check if there's already a column called geometry
            newheader.append('geometry')
            writer.writerow(newheader)

            for row in data:
                wkt_string = row[colindex]
                outrow = row
                jrstring = jrstring_from_wkt(wkt_string)
                outrow.append(jrstring)
                writer.writerow(outrow)
        print(f'created output file at: {of}')
        
def jrstring_from_wkt(wktstring):
    """Produces a JavaRosa string from a Well-Known Text string.
    For now, doing this with pure Python string manipulation rather than using
    a proper GIS library to parse the WKT. This probably makes it less useful
    for more general use (it'll quite possibly fall over when confronted with
    some perfectly valid WKT), but for creating entity lists for ODK from 
    digitized buildings, this is faster and avoids creating dependencies.
    Args:
        jrstring (str): 
    Returns:
        str: Javarosa geometry; nodes consisting of space-delimited strings of 
        lat, lon, elevation, accuracy, each node separated by a semicolon
    """
    # TODO: implement

    print(wktstring)
    nodes = wktstring.strip().split(',')
    coordstrings = [node
                    .replace('POLYGON ((', '')
                    .replace('))','')
                    for node in nodes]

    coordsflipped = [f'{x.split()[1]} {x.split()[0]} 0.0 0.0' for x in coordstrings]
    jrstring = ';'.join(coordsflipped)
    print(jrstring)
    return jrstring
    
    
def wkt_column_index_from_header(infile, headername):
    """Returns a 1-based column index for a column in a CSV file with 
    a particular name.
    Args:
        infile (filepath): The relevant CSV file
        header name (str): The header name to search for
    Returns:
        int: the 1-based column number.
    """
    # Not implemented yet, specify yer own column header
    pass
    

if __name__ == "__main__":

    p = argparse.ArgumentParser()

    p.add_argument('infile', help = "Input CSV file")
    p.add_argument('-c', '--column', help =
                   'Column containing the WKT to be converted to JavaRosa')
    p.add_argument('-cn', '--column_name', default = 'geotrace', help =
                   'The header of the column containing the WKT'
                   ' to be converted to JavaRosa')
    p.add_argument('-d', '--delimiter', default = ',', help =
                   'Token delimiting one value from the next, usually , or ;')
    p.add_argument('-o', '--output', help = 'Output file path')
    a = p.parse_args()

    convert_to_javarosa(a.infile, a.column, a.column_name,
                        a.delimiter, a.output)
