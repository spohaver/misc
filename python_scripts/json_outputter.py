#!/usr/bin/python
''' Author: Sean O'Haver
    Desc: In response to times where you don't have jq available, a script that
          will pretty print json data, built for python 2.7
'''
from __future__ import print_function
import json
import sys
from optparse import OptionParser

def json_load(filename):
    ''' Load up json data
    filename: filename location to load json data
    '''
    try:
        with open(filename) as datafile:
            json_data = json.load(datafile)
    except ValueError as val_err:
        print("Could not parse JSON from {filename}\nError:{err}".format(
                filename=filename,
                err=val_err
                ),
            file=sys.stderr
            )
        sys.exit(1)
    return json_data

def optparser():
    ''' Lets parse some args, arrrg '''
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--filename", help="json file")
    parser.add_option("-i", "--indent",
            default=4,
            help="Number of spaces for indention"
            )
    parser.add_option("-s", "--sort", 
            action="store_true",
            default=False,
            help="Sort the keys"
            )
    parser.add_option("-m", "--minimal",
            action="store_true",
            default=False,
            help="Use minimal separators to shorten whitespace (',',':')"
            )
    parser.add_option("-v", "--verbose",
            action="store_true",
            default=False,
            help="Print out args given and explanations"
            )
    (options, args) = parser.parse_args()
    if not options.filename and sys.stdin.isatty():
        parser.error("No JSON Data Found")
    try:
        int(options.indent)
    except ValueError:
        parser.error("{value} is not an integer!".format(
            value=options.indent)
            )
    if options.verbose:
        print("Options: {0}".format(options))
    return options

def main():
    options = optparser()
    if options.filename:
        json_data = json_load(options.filename)
    else:
        if not sys.stdin.isatty():
            json_data = json.load(sys.stdin)
    if options.minimal:
        if options.verbose:
            print("Indent Value {value} ignored..".format(
                value=options.indent)
                )
        print(json.dumps(
                json_data,
                separators=(',',':'),
                sort_keys=options.sort,
                )
        )
    else:
        print(json.dumps(
                json_data,
                sort_keys=options.sort,
                indent=int(options.indent)
                )
        )
    return 0

if __name__ == "__main__":
   sys.exit(int(main()))

