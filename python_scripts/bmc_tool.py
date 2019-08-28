#!/usr/bin/env python
# author: Sean O'Haver (spohaver@gmail.com)
# desc: A bmc tool for those who have multiple vendors of bmc's, will loop through
#       vendor dicts until one works, or exits if none work.
import argparse
import logging
import os
import re
import shlex
import sys
from subprocess import PIPE, run

_VERSION = 0.1

# CONSTANTS
COMMANDS = { 'r': 'mc reset cold',
             'l': 'lan print',
             'i': 'mc info',
             's': 'sel list',
             'a': 'sol activate',
             'd': 'sol deactivate',
             '1': 'chassis power status',
             '2': 'chassis power reset',
             '3': 'chassis power cycle',
             '4': 'chassis power off',
             '5': 'chassis power on',
             'q': 'quit'
}
OPTIONS = '-I lanplus'
CREDS = {
    'vendor1': {
        'user': 'username',
        'file': '/foo/bar/baz'
    },
    'vendor2': {
        'user': 'admin',
        'file': '/tmp/foobar'
    }
}

LOG = logging.getLogger(__name__)

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


def run_cmd(cmd, timeout=60):
    """ Run a single shell command, split via shlex with a timeout
    :param cmd: Command to run
    :type cmd: str
    :param timeout: Timeout in seconds, default=60
    :type timeout: int
    :return: stdout or stderr based on return code of the command
    :rtype: str
    """
    p = run(shlex.split(cmd),
            stdout=PIPE,
            stderr=PIPE,
            encoding='utf-8',
            timeout=timeout)
    # if not p.check_returncode():
    if p.returncode == 0:
        return p.stdout
    else:
        LOG.warn("Command {0} returned {1}:".format(cmd, p.returncode))
        return False


def run_ipmicmd(user, filename, hostname, cmd, options=OPTIONS):
    """ wrapper for run_cmd for ipmitool commands
    :param user: username used for ipmitool
    :type user: str
    :param filename: filename to be passed to ipmitool that has pw
    :type filename: str
    :param hostname: Hostname
    :type hostname: str
    :param cmd: command to be run via ipmitool
    :type cmd: str
    :return run_cmd(ipmi_cmd): returns output of ipmitool cmd
    :return type: str
    """
    ipmi_cmd = ('ipmitool {options} -U {user} -f {filename} -H {hostname} '
                '{cmd}'.format(options=options,
                               user=user,
                               filename=filename,
                               hostname=hostname,
                               cmd=cmd
                               )
    )
    LOG.debug('Running {0}'.format(ipmi_cmd))
    return run_cmd(ipmi_cmd)


def validate_fqdn(hostname):
    """ Validate hostname is a fqdn, simple validation based on
    https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch08s15.html
    :param hostname: hostname to validate
    :type hostname: str
    :return: True if hostname comes up with regex match, False if not a match
    :rtype: bool
    """
    if hostname.endswith('.'):
        hostname = hostname[:-1]
        if len(hostname) < 1 or len(hostname) > 253:
            return False
    compile_string = '^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
    r = re.compile(compile_string, re.IGNORECASE)
    if r.match(hostname):
        LOG.debug('{0} validated'.format(hostname))
        return True
    else:
        LOG.debug('{0} could not be validated'.format(hostname))
        return False


def parse_args():
    """ Parse all the things args based """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'hostname',
        help='bmc hostname/ip address'
    )
    args = parser.parse_args()
    if validate_fqdn(args.hostname):
        LOG.debug('returning args: {0}'.format(args))
        return args
    else:
        LOG.error('{0} is not a valid hostname. Exiting'.format(args.hostname))
        sys.exit(1)


def menu_selection(hostname):
    """ Display menu based on COMMANDS available
    :param hostname: Hostname
    :type hostname: str
    :return Commands[answer]: Command to be run via ipmitool
    :return type: str
    """
    answer = ""
    while answer not in COMMANDS:
        print('BMC TOOL ver {0}'.format(_VERSION))
        print('HOSTNAME: {0}'.format(hostname))
        print('Command Selection Menu:')
        for key in COMMANDS:
            print("{}:  {}".format(key, COMMANDS[key]))
        answer = input('Selection: ')
    if answer == 'q':
        sys.exit(0)
    else:
        return COMMANDS[answer]


def get_creds(hostname):
    """ Get credentials for BMC
    :param hostname: Hostname
    :type hostname: str
    :return vendor, CREDS[vendor]['user'], CREDS[vendor]['file']: vendor, user, and filename
    :return type: string (3 variables)
    """
    for vendor in CREDS:
        if not os.path.exists(CREDS[vendor]['file']):
            LOG.error('{0} does not exist, are you running this from the right '
                  'host? Exiting'.format(CREDS[vendor]['file']))
            sys.exit(2)
        cmd = 'chassis power status'
        if run_ipmicmd(CREDS[vendor]['user'],
                       CREDS[vendor]['file'],
                       hostname,
                       cmd):
            LOG.debug('Returning {0}, {1}, {2}'.format(
                vendor, CREDS[vendor]['user'], CREDS[vendor]['file']))
            return vendor, CREDS[vendor]['user'], CREDS[vendor]['file']
        else:
            LOG.warn('{0} did not work, continuing..'.format(vendor))
    LOG.error('Ran out of vendors, exiting')
    sys.exit(3)


def main():
    """ Main """
    args = parse_args()
    vendor, user, filename = get_creds(args.hostname)
    # Bring up menu of options
    while True:
        cmd = menu_selection(args.hostname)
        print('{0}\n\n'.format(run_ipmicmd(user,
                                           filename,
                                           args.hostname,
                                           cmd)))

if __name__ == '__main__':
    setup_logging()
    if os.geteuid() == 0:
        sys.exit(int(main()))
    else:
        LOG.error(
            "This script needs to be run with administrative privileges"
        )
        sys.exit(1)
