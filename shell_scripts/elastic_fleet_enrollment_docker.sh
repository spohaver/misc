#!/usr/bin/env bash
# Quick script to test out Elastic Cloud Fleet Enrollments


fleet_server_host_url=$1
enrollment_token=$2
version=8.4.1-amd64
docker pull docker.elastic.co/beats/elastic-agent:${version}

docker run \
  --env FLEET_ENROLL=1 \
  --env FLEET_URL=${fleet_server_host_url} \
  --env FLEET_ENROLLMENT_TOKEN=${enrollment_token} \
  --rm docker.elastic.co/beats/elastic-agent:${version}
