#!/usr/bin/python3
"""
Creates a dict from an XML file
"""

import xml.etree.ElementTree as etree
import sys

def main(infile):
    xmlFile = etree.parse(sys.argv[1])
    root = xmlFile.getroot()
    for child in root[0][1][0][0]:
        if '}' in child.tag:
            tag = child.tag.split('}')[1]
        else:
            tag = child.tag
        print(tag)
    
    
if __name__ == "__main__":
    
    main(sys.argv[1])
