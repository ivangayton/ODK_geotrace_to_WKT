#!/usr/bin/python3
"""
Scan a folder full of ODK xml/json and push out a csv
"""

import sys, os
import csv
import json
from lxml import etree

def scandir(dir, ext):
    """Walk through a directory and return a list of all files of type .ext"""
    filelist = []
    for path, dirs, files in os.walk(dir):
        for f in files:
            if(os.path.splitext(f)[1]==ext):
                filelist.append(os.path.join(path, f))
    return filelist

def main(model, indir, outfile):
    """Produce an output CSV containing all the data in all ODK submissions 
    corresponding to the fields in the model file (a CSV with the headers only)
    """

    file_type = '.json'
    data_files = scandir(indir, file_type)    
    fields = []
    
    try:
        model_csv = open(model)
        linereader = csv.reader(model_csv, delimiter = ',')
        fields = next(linereader)
    except:
        print('Something is wrong with your input model')
        exit()

    with open(outfile, 'w') as out_file:
        writer = csv.writer(out_file, delimiter = ',')
        
        # Insert the header row first
        fields.append('lat')
        fields.append('lon')
        fields.append('osm_xml')
        writer.writerow(fields)

        for f in data_files:
            # Add data to CSV
            json_dict = {}
            newline =[]
            try:
                json_dict = json.loads(open(f).read())
            except:
                print('Something is wrong with {}'.format(f))
            for field in fields:
                if field in json_dict:
                    newline.append(json_dict[field])
                else:
                    if field != 'osm_xml' and field != 'lat' and field != 'lon':
                        newline.append('')

            # Grab contents of associated OSM file, if such a file exists 
            if 'osm_building' in json_dict:
                osm_file = os.path.join(os.path.dirname(f),json_dict['osm_building'])
                try:
                    # Add lat and long (first node only if building polygon)
                    xml_body = etree.parse(osm_file)
                    root = xml_body.getroot()
                    firstlatlong = []
                    for child in root:
                        firstlatlong.append(child.get("lat"))
                        firstlatlong.append(child.get("lon"))
                    newline.append(firstlatlong[0])
                    newline.append(firstlatlong[1])

                    # Add full text of .osm file as final field
                    f = open(osm_file)
                    xml_text = f.read()
                    newline.append(xml_text)
                except:
                    print('something is wrong with {}'.format(osm_file))
                        
            writer.writerow(newline)                    

if __name__ == "__main__":
    #TODO set this up with argparse and a default outfile
    model = sys.argv[1]
    indir = sys.argv[2]
    outfile = sys.argv[3]
    main(model, indir, outfile)
