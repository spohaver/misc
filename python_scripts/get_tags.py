#!/usr/bin/env python3
import argparse
import json
import os
import requests
import sys


DESC = """Gets the env tags from AWS metatadata.
    REQUIRES: 'Allow tags in instance metadata' enabled"""
METADATA_URL = 'http://169.254.169.254'
URI_TAGS = 'latest/meta-data/tags/instance'


def parse_envs(json_data):
    """ Parses envs into a dictionary, envs should be in JSON format """
    return json.loads(json_data)


def parse_args():
    """ Parse all the things args based """
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument(
        'tag',
        default='envs',
        help='Tag we want to grab from instance meta-data',
        nargs='?'
    )
    parser.add_argument(
        '--all-tags',
        '-a',
        action='store_true',
        help='Grab all the tags from instance meta-data',
        default=False
    )
    parser.add_argument(
        '--export-tags',
        '-e',
        action='store_true',
        help='Export tags that can be used in eval/bash',
        default=False
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    env_vars = {}
    if args.all_tags:
        uri = os.path.join(METADATA_URL, URI_TAGS)
        tags = requests.get(uri).text.split('\n')
        for tag in tags:
            uri = os.path.join(METADATA_URL, URI_TAGS, tag)
            env_vars[tag] = requests.get(uri).text
    else:
        uri = os.path.join(METADATA_URL, URI_TAGS, args.tag)
        if args.tag == 'envs':
            env_vars = parse_envs(requests.get(uri).json)
        else:
            env_vars[args.tag] = requests.get(uri).text
    if args.export_tags:
        os_envs = dict(os.environ).keys()
        for tag in env_vars.keys():
            if tag not in os_envs:
                print('export {0}="{1}"'.format(tag.upper(), env_vars[tag]))
            else
                # DO NOT override system set environment variables, commented out
                print('#export {0}="{1}"'.format(tag.upper(), env_vars[tag]))
    else:
        print("Tags and values")
        for tag in env_vars.keys():
            print('{0}: {1}'.format(tag, env_vars[tag]))
    return 0


if __name__ == '__main__':
    sys.exit(int(main()))
