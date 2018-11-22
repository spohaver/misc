#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys
from json import dumps, load, loads
from yaml import safe_dump

def json_load(filename):
    ''' Load up json data

    :param filename: filename location to load json data
    :type filename: str

    :return: json dump from json datafile
    :rtype: dict(json)
    '''
    try:
        with open(filename) as datafile:
            json_data = load(datafile)
    except ValueError, val_err:
        print("Could not parse JSON from {filename}\nError:{err}".format(
                filename=filename,
                err=str(val_err)
                ),
            file=sys.stderr
            )
        sys.exit(1)
    return json_data

def yaml_out(message, block_style=True):
    '''Returns yaml output from a json input

    :param message: json message
    :type message: dict(json)

    :param block_style: Print out block style yaml (Default: True)
    :type block_style: bool
    '''

    try:
        jsondata = loads(message)
    except ValueError, e:
        print('Could not load the message: {0}\nerror: {1}'.format(message, str(e)))
    except TypeError:
        try:
            jsondata = loads(dumps(message))
            mesage = dumps(message)
        except:
            print('Could not load the message: {0}'.format(message))

    if block_style is True:
        print(safe_dump(message, allow_unicode=True, default_flow_style=False))
    else:
        print(safe_dump(message, allow_unicode=True))

def parse_args():
    parser = argparse.ArgumentParser()
    #parser.add_argument('-f', '--filename', help='blah')
    parser.add_argument(
            '-f',
            '--filename',
            help='Filename')
    parser.add_argument(
            '--input',
            type=argparse.FileType('r'),
            default='-',
            help='std input'
            )
    args = parser.parse_args()
    return args

def main():
    '''Need to focus on json file and piped json output'''
    args = parse_args()
    if args.filename:
        message = json_load(args.filename)
    else:
        message = load(args.input)
    yaml_out(message)

if __name__ == '__main__':
    exit(main())
