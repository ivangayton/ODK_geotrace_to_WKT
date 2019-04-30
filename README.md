# Convert ODK Geotraces to Well-Known Text linestrings

Takes a CSV file containing line strings from an OpenDataKit Geotrace, which
consist of a series of text coordinates, and returns a similar CSV file with 
properly formatted Well-Known Text (WKT) linestrings (and points).

**Positional Argument:**

  1) An input CSV file

**Optional Arguments:**
  - -c or --column: An integer specifying which column contains the geotrace (1-based column count; the way humans, not computers, count). No default value; if this parameter is not given the script assumes that the appropriate column is named rather than numbered (see next argument).
  - -cn or --column_name: a string matching the column header of the geotrace column. Defaults to ```drain_line``` because the Ramani Huria team is using it for drain traces.
  - -d or --delimiter: a single character representing the delimiter of the CSV file (usually a comma, semicolon, or Tab character). Defaults to assuming a comma.
  - -o our --output: the name of the output file. Defaults to creating a file with the same name as the input file, with _results appended. So ```/my/input/file.csv``` will by default get an output file ```/my/input/file_results.csv```.
  
**Example usage:**

```python3 lines_to_wkt.py infile.csv``` Looks for a column named "drain_lines" and converts the linestrings in it to WKT.

```python3 lines_to_wkt.py infile.csv -c 8``` Converts the contents of the 8th column (starting from 1) into WKT from linestrings.

```python3 lines_to_wkt.py infile.csv -cn road_trace -d ;``` Looks for a column titled "road_trace". Expects the CSV delimiter to be a semicolon rather than a comma (KoBo Toolbox uses semicolons by default, while OMK Server uses commas). 

___

This script expects the default GeoTrace format from an ODK CSV export from
an ODK aggregator (ODK Aggregate, Kobo Toolbox, or OMK Server), which consists of a series of node coordinates separated by semicolons. Each node seems to consist of a latitude, longitude, and two zeros, internally separated by spaces. The WKT format specifies the type (LINESTRING or POINT) followed by long, then lat separated by spaces, then a comma separating nodes.

The output file should be identical to the input, with the exception of having converted the GeoTrace coordinates to valid WKT lines.

In a future version this may allow additional column number arguments to convert multiple traces in the same file (in case someone collects multiple lines in the same survey).