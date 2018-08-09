#!/usr/bin/python3
"""Scan a folder full of ODK xml and push out a csv
"""

import sys, os
import csv
import json

def scandir(dir, ext):
    filelist = []
    for path, dirs, files in os.walk(dir):
        for f in files:
            if(os.path.splitext(f)[1]==ext):
                filelist.append(os.path.join(path, f))
    return filelist

def main(model, indir, outfile):
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

    print(fields)

    with open(outfile, 'w') as out_file:
        writer = csv.writer(out_file, delimiter = ',')
        writer.writerow(fields)
        for f in data_files:
            # Add data to CSV
            json_dict = {}
            newline = []
            try:
                json_dict = json.loads(open(f).read())
            except:
                print('Something is wrong with {}'.format(f))
            for field in fields:
                if field in json_dict:
                    newline.append(json_dict[field])
                else:
                    newline.append('')
            writer.writerow(newline)
                    

if __name__ == "__main__":
    model = ('/home/ivan/Documents/01 HOT/01 Ramani Huria/Data Collection/'
             'GWPL_Trash/GWPL_Client_Tagging_V2.csv')
    indir = ('/home/ivan/Documents/01 HOT/01 Ramani Huria/Data Collection/'
             'GWPL_Trash/odk/instances')
    outfile = ('/home/ivan/Documents/01 HOT/01 Ramani Huria/Data Collection/'
             'GWPL_Trash/GWPL_Client_Tagging_V2_RESULTS.csv')
    main(model, indir, outfile)
