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
    model = sys.argv[1]
    indir = sys.argv[2]
    outfile = sys.argv[3]
    main(model, indir, outfile)
