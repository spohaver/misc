#!/usr/bin/env python3
# author: spohaver
# description: Creates a webtoken URL based on the user credentials
import argparse
import boto3
import sys


# Constants
ALB = ''

def check_credentials():
    """ Use boto3's Security Token Service (STS)'s get_caller_identity to
        validate credentials, this allows for both env vars and credentials
        stored in $HOME/.aws
    """
    sts = boto3.client('sts')
    try:
        user_creds = sts.get_caller_identity()
    except boto3.exceptions.botocore.exceptions.NoCredentialsError:
        print('No AWS credentials found', file=stderr)
        raise
    except boto3.exceptions.botocore.exceptions.ClientError as err:
        print('Invalid AWS credentials -- Client Error: {0}'.format(err),
              file=stderr
              )
        raise
    return True


def mwaa_client(mwaa_env):
    """ Use boto3's MWAA client to create a webtoken and returns a tuple
        with hostname and webtoken
    """
    mwaa = boto3.client('mwaa')
    response = mwaa.create_web_login_token(Name=mwaa_env)
    webServerHostName = response["WebServerHostname"]
    webToken = response["WebToken"]
    #return airflowUIUrl
    return (webServerHostName, webToken)


def parse_args():
    """ Parse all the things args based """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mwaaenv',
        help='MWAA Environment Name'
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if check_credentials:
        hostname, webToken = mwaa_client(args.mwaaenv)
        if ALB:
            airflowUIUrl = 'https://{0}/aws_mwaa/aws-console-sso?login=true#{1}'.format(
                ALB,
                webToken
            )
        else:
            airflowUIUrl = 'https://{0}/aws_mwaa/aws-console-sso?login=true#{1}'.format(
                webServerHostName,
                webToken
            )
        print("Here is your Airflow UI URL: ")
        print(airflowUIUrl)
    return 0


if __name__ == '__main__':
    sys.exit(int(main()))
