#!/usr/bin/env python3
import argparse
import json
import os
import requests
import sys


DESC = """Gets the env tags from AWS metatadata.
    REQUIRES: 'Allow tags in instance metadata' enabled.
    Note: default tag that pulls is 'envs', value must be in JSON format"""
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
        help='tag we want to grab, default="envs"',
        nargs='?'
    )
    parser.add_argument(
        '--all-tags',
        action='store_true',
        help='grab all the tags',
        default=False
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    env_vars = {}
    print(args)
    if args.all_tags:
        uri = os.path.join(METADATA_URL, URI_TAGS)
        print('URI: ', uri)
        print('Request response: ', requests.get(uri).text)
        tags = requests.get(uri).text.split('\n')
        print('tags: ', tags)
        for tag in tags:
            uri = os.path.join(METADATA_URL, URI_TAGS, tag)
            print('URI: ', uri)
            env_vars[tag] = requests.get(uri).text
    else:
        uri = os.path.join(METADATA_URL, URI_TAGS, args.tag)
        print('URI: ', uri)
        if args.tag == 'envs':
            env_vars = parse_envs(requests.get(uri).json)
        else:
            env_vars[args.tag] = requests.get(uri).text
    print(env_vars)
    return 0


if __name__ == '__main__':
    sys.exit(int(main()))
