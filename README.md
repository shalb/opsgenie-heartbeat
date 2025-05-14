# opsgenie-heartbeat
opsgenie heartbeat for prometheus monitoring

## Info

Use this container if you use opsgennie heartbeat

## Install

```bash
# Add Opsgenie api key to secret and deploy it, see example examples/helmfile/example-secret.yaml
# Install helm chart
helm repo add opsgenie-heartbeat https://raw.githubusercontent.com/shalb/opsgenie-heartbeat/master/charts/
helm repo update
helm -n monitoring install opsgenie-heartbeat opsgenie-heartbeat/opsgenie-heartbeat -f opsgenie-heartbeat.yaml --version 0.0.6
```

## build

```bash
docker login
docker-compose -f docker-compose-build.yml build
docker-compose -f docker-compose-build.yml push
```

## configuration

Customize your configuration via config file entrypoint/entrypoint.py.yml

## run

Use docker-compose.yml to run container with env file opsgenie-heartbeat/env_secrets
```bash
docker-compose up
```

## prepare helm chart

```bash
helm package examples/helmfile/opsgenie-heartbeat/
mv opsgenie-heartbeat-0.0.6.tgz charts/
helm repo index charts --url https://raw.githubusercontent.com/shalb/opsgenie-heartbeat/master/charts/
```

## dependencies if want to run without container

```bash
pip3 install --user pyaml prometheus_client
```

