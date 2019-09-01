# A place to store my commonly used functions
import json
import re
import shlex
import sys
from subprocess import run, PIPE


def json_load(filename):
    """ Load up json data
    :param filename: filename location to load json data
    :type filename: str
    :return: Returns json data as a dictionary
    :rtype: dict
    """
    try:
        with open(filename) as datafile:
            json_data = json.load(datafile)
    except ValueError as val_err:
        print(
            "Could not parse JSON from {filename}\nError:{err}".format(
                filename=filename,
                err=val_err
                ),
            file=sys.stderr
            )
        sys.exit(1)
    return json_data


def json_write(json_data, filename, indent=4):
    """ Write json data to filename
    :param json_data: json to be written
    :type json_data: dict
    :param filename: name of filename to be written
    :type filename: str
    :return: defaults to return True (if converted to int will be 1)
    :rtype: bool
    """
    with open(filename, 'w') as datafile:
        json_data = json.dump(json_data, datafile, indent=indent)
    return True


def run_cmd(cmd, timeout=60, shell=False):
    """ Run a single shell command, split via shlex with a timeout
    :param cmd: Command to run
    :type cmd: str
    :param timeout: Timeout in seconds, default=60
    :type timeout: int
    :param shell: False=run under existing session,
                  True=run under sub-session(Potential Security Risk)
    :type shell: bool
    :return: stdout or stderr based on return code of the command
    :rtype: str
    """
    p = run(shlex.split(cmd),
            shell=shell,
            stdout=PIPE,
            stderr=PIPE,
            encoding='utf-8',
            timeout=timeout)
    # if not p.check_returncode():
    if p.returncode == 0:
        return p.stdout
    else:
        print("Command {0} returned {1}:".format(cmd, p.returncode))
        return p.stderr


def validate_fqdn(hostname):
    """
    Validate hostname is a fqdn, simple validation based on
    https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch08s15.html
    :param hostname: hostname to validate
    :type hostname: str
    :return: True if hostname comes up with regex match, False if not a match
    :rtype: bool
    """
    if hostname.endswith ('.'):
        hostname = hostname[:-1]
        if len(hostname) < 1 or len(hostname) > 253:
            return False
    compile_string = '^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
    r = re.compile(compile_string, re.IGNORECASE)
    if r.match(hostname):
        return True
    else:
        return False
