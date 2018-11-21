import sys
from json import dumps, loads
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
        error('Could not load the message: {0}\nerror: {}'.format(message, e))
    except TypeError:
        try:
            jsondata = loads(message)
        except ValueError, e:
            error('Could not load the message: {0}\nerror: {}'.format(message, e))
    if block_style:
        print safe_dump(message, allow_unicode=True, default_flow_style=False)
    else:
        print safe_dump(message, allow_unicode=True)

def main():
    '''Need to focus on json file and piped json output'''
    yaml_out(message)

if __name__ == '__main__':
    exit(main)
