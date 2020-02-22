# Convert ODK Geotraces to GIS-friendly formats (WKT linestrings or 3D points)

Takes a CSV file containing line strings from an OpenDataKit Geotrace, which
consist of a series of text coordinates, and returns a similar CSV file with 
properly formatted Well-Known Text (WKT) linestrings (and points).

These scripts expect the default GeoTrace format from an ODK CSV export from
an ODK aggregator (ODK Aggregate, Kobo Toolbox, or OMK Server), which consists of a series of node coordinates separated by semicolons. Each node seems to consist of a latitude, longitude, and two zeros, internally separated by spaces. The WKT format specifies the type (LINESTRING or POINT) followed by long, then lat separated by spaces, then a comma separating nodes.



## ```lines_to_wkt``` usage
**Positional Argument:**

  1) An input CSV file

**Optional Arguments:**
  - -c or --column: An integer specifying which column contains the geotrace (1-based column count; the way humans, not computers, count). No default value; if this parameter is not given the script assumes that the appropriate column is named rather than numbered (see next argument).
  - -cn or --column_name: a string matching the column header of the geotrace column. Defaults to ```geotrace``` because that might occasionally be the actual column header used.
  - -d or --delimiter: a single character representing the delimiter of the CSV file (usually a comma, semicolon, or Tab character). Defaults to assuming a comma.
  - -o our --output: the name of the output file. Defaults to creating a file with the same name as the input file, with _results appended. So ```/my/input/file.csv``` will by default get an output file ```/my/input/file_results.csv```.
  
**Example usage:**

```python3 lines_to_wkt.py infile.csv``` Looks for a column named "geotrace" and converts the linestrings in it to WKT.

```python3 lines_to_wkt.py infile.csv -c 8``` Converts the contents of the 8th column (count starting from 1) into WKT from linestrings.

```python3 lines_to_wkt.py infile.csv -cn road_trace -d ;``` Looks for a column titled "road_trace". Expects the CSV delimiter to be a semicolon rather than a comma (KoBo Toolbox uses semicolons by default, while OMK Server uses commas). 

The output file should be identical to the input, with the exception of having converted the GeoTrace coordinates to valid WKT lines.

In a future version this may allow additional column number arguments to convert multiple traces in the same file (in case someone collects multiple lines in the same survey).

___

## ```points_3D_from_ODK_lines``` usage
**Positional Argument:**

  1) An input CSV file

**Optional Arguments:**
  - -c or --column: An integer specifying which column contains the geotrace (1-based column count; the way humans, not computers, count). No default value; if this parameter is not given the script assumes that the appropriate column is named rather than numbered (see next argument).
  - -cn or --column_name: a string matching the column header of the geotrace column. Defaults to ```geotrace``` because why not.
  - -d or --delimiter: a single character representing the delimiter of the CSV file (usually a comma, semicolon, or Tab character). Defaults to assuming a comma.
  - -o our --output: the name of the output file. Defaults to creating a file with the same name as the input file, with _3D_points appended. So ```/my/input/file.csv``` will by default get an output file ```/my/input/file_3D_points.csv```.
  - -kc or --keep_columns: a string describing which columns in the _original_ file (which has one row per geotrace line) should be kept in the output file (which has one row per point in those geotrace lines). It seems obvious that users don't want to duplicate all of the information about each geotrace line, but probably want to retain some of it (for example, the line ID or the ID of the device that did the survey). 
  
**Example usage:**

```python3 points_3D_from_ODK_lines.py infile.csv``` Looks for a column named "geotrace", extracts the 3-dimensional points from the lines, and exports a new CSV file with a row for each point in all lines.

```python3 points_3D_from_ODK_lines.py infile.csv -c 8``` Converts the contents of the 8th column (starting from 1) into 3D points from linestrings.

```python3 points_3D_from_ODK_lines.py infile.csv -cn river_transect -d ;``` Looks for a column titled "road_trace". Expects the CSV delimiter to be a semicolon rather than a comma (KoBo Toolbox uses semicolons by default, while OMK Server uses commas). 

```python3 points_3D_from_ODK_lines.py infile.csv -c 17 -kc 3,6-9,22``` produces a csv file full of 3D points, and includes columns 3, 6, 7, 8, 9, and 22 from the original file, along with the lat, long, elevation, and precision of each individual point.
___
