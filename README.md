# opsgenie-heartbeat
opsgenie heartbeat for prometheus monitoring

## Info

Use this container if you use opsgennie heartbeat

## build

~~~~
docker login
docker-compose -f docker-compose-build.yml build
docker-compose -f docker-compose-build.yml push
~~~~

## configuration

Customize your configuration via config file entrypoint/entrypoint.py.yml

## run

Use docker-compose.yml to run container with env file opsgenie-heartbeat/env_secrets
~~~~
docker-compose up
~~~~

## prepare helm chart

~~~~
helm package examples/helmfile/opsgenie-heartbeat/
mv opsgenie-heartbeat-0.0.1.tgz charts/
helm repo index charts --url https://raw.githubusercontent.com/shalb/opsgenie-heartbeat/master/charts/
~~~~

## dependencies if want to run without container

pip3 install --user pyaml prometheus_client

