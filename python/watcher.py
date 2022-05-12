#!/usr/bin/env python3
# Description: watches a directory for changes
import argparse
import logging
import os
import sys
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


DESC = """ Watches a directory for changes and will act on creation
"""
LOG = logging.getLogger(__name__)
LOGLEVEL = logging.INFO


def parse_args():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument(
        '-d', '--directory',
        default='',
        help='Directory to watch',
    )
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        default=False,
        help='Recursively watch in sub-directories',
    )
    args = parser.parse_args()
    return args


def setup_logging(
    logformat='[%(asctime)s] - %(levelname)s - %(message)s',
    level=logging.INFO,
    log=LOG,
    stream=sys.stdout,
):
    handler = logging.StreamHandler(
        stream=stream,
    )
    fmt = logging.Formatter(logformat)
    handler.setFormatter(fmt)
    log.addHandler(handler)
    log.setLevel(level)
    LOG.debug('logging setup')
    return True


class Watcher():

    def __init__(self, watch_dir='', recursive=False):
        self.observer = Observer()
        if not watch_dir:
            self.watch_dir = os.path.expanduser('~')
        else:
            self.watch_dir = watch_dir
        if recursive:
            self.recursive=True
        else:
            self.recursive=False

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler,
            self.watch_dir,
            recursive=self.recursive
        )
        LOG.info('Watcher starting')
        self.observer.start()
        try:
            while True:
                sleep(2)
        except:
            self.observer.stop()
            LOG.warning('Watcher stopped unexpectedly')
        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        if event.event_type == 'created':
            LOG.info('File created:  {0}'.format(event.src_path))

        if event.event_type == 'modified':
            LOG.info('File modified: {0}'.format(event.src_path))


if __name__ == '__main__':
    setup_logging()
    args = parse_args()
    watcher = Watcher(args.directory, args.recursive)
    watcher.run()
