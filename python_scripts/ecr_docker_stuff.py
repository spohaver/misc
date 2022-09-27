#!/usr/bin/env python3
import base64
import boto3
import docker

REGION = ''  # AWS Region name (ie. us-east-1, us-west-2)
AWS_ACCOUNT = ''
ECR_REGISTRY = ''
ENVS = {
        'NODE_ENV': 'development',
}


def docker_login():
    """ ecr get_authorization_token returns base64 encoded byte string
        prefixed with username, looks like 'AWS:'
        returns docker_client, a logged instantiation of docker client
    """
    ecr = boto3.client('ecr', region_name=REGION)
    token = ecr.get_authorization_token()['authorizationData'][0]['authorizationToken']
    decoded = base64.b64decode(token).decode('utf-8').replace('AWS:', '')
    #start docker client
    docker_client = docker.from_env()
    docker_client.login(username='AWS', password=decoded, registry=ECR_REGISTRY)
    return docker_client


def docker_run(cmd, envvars, docker, image, repo, tag):
    """ Runs docker based on command and envvars
    cmd (string)    - Command to be run
    envvars (dict)  - dictionary of environment variables to pass into the container
    docker (object) - Instantiated Docker Client
    image (string)  - Image name
    repo (string)   - Repo Name
    tag (string)    - Image tag (ie. latest)
    """
    image = docker.images.pull(
        repository='{0}/{1}'.format(ECR_REGISTRY, repo),
        tag='{0}'.format(tag)
    )
    docker.containers.run(
        image=image,
        command=cmd,
        environment=envvars,
        remove=True,
        #stdin_open=True,
        #tty=True
    )
