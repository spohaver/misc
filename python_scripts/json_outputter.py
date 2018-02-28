#!/usr/bin/python
''' Author: Sean O'Haver
    Desc: In response to times where you don't have jq available, a script that
          will pretty print json data
    TODO: Add try/except blocks to catch non json output
'''
import json
import sys
from optparse import OptionParser

def json_load(input_data):
    ''' Load up json data
    input_data: data from stdin or file
    '''
    with open(input_data) as datafile:
        json_data = json.load(datafile)
    return json_data


def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--filename", help="json file")
    parser.add_option("-i", "--indent", default=4,
                      help="Number of spaces for indention")
    parser.add_option("-s", "--sort", action="store_true",
                      default=False, help="Sort the keys")
    (options, args) = parser.parse_args()
    if options.filename:
        json_data = json_load(options.filename)
    else:
        if not sys.stdin.isatty():
            json_data = json.load(sys.stdin)
        else:
            parser.error("No JSON Data Found")
    print json_data
    print json.dumps(json_data,sort_keys=options.sort,indent=int(options.indent))
    return 0

if __name__ == "__main__":
   sys.exit(int(main()))

