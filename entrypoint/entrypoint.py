#!/usr/bin/env python

import prometheus_client
import prometheus_client.core
import traceback
import argparse
import sys
import time
import logging
import yaml
import datetime
import os
import subprocess
import urllib
import http.server

# pip3 install prometheus_client docker pyaml

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--config', default=sys.argv[0] + '.yml', help='config file location')
parser.add_argument('--log_level', help='logging level')
args = parser.parse_args()

# add prometheus decorators
REQUEST_TIME = prometheus_client.core.Summary('request_processing_seconds', 'Time spent processing request')

def get_config(args):
    '''Parse configuration file and merge with cmd args'''
    for key in vars(args):
        conf[key] = vars(args)[key]
    with open(conf['config']) as conf_file:
        conf_yaml = yaml.load(conf_file, Loader=yaml.FullLoader)
    for key in conf_yaml:
        if not conf.get(key):
            conf[key] = conf_yaml[key]

def configure_logging():
    '''Configure logging module'''
    log = logging.getLogger(__name__)
    log.setLevel(conf['log_level'])
    FORMAT = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(format=FORMAT)
    return log

# Decorate function with metric.
@REQUEST_TIME.time()
def get_data():
    '''Get data from target service'''
    req = urllib.request.Request(conf['prometheus_test_url'])
    responce = urllib.request.urlopen(req)
    raw_data = responce.read().decode()
    if 'prometheus_notifications_errors_total' in raw_data:
        if send_heartbeat():
            return True

def send_heartbeat():
    '''Get data '''
    # create config
    opsgenie_lamp_config = 'apiKey={0}\nconnectionTimeout=10\nrequestTimeout=10\n'.format(os.environ['OPSGENIE_API_KEY'])
    if not os.path.exists(conf['config_name']):
        with open(conf['config_name'], 'w') as opsgenie_lamp_config_file:
            opsgenie_lamp_config_file.write(opsgenie_lamp_config)
    command_tmp = '/opt/opsgenie_lamp/lamp heartbeat --config {0} --name monitoring_{1}_prometheus'
    command = command_tmp.format(conf['config_name'], os.environ['PROJECT']).split()
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait(timeout=10)
    stdout, stderr = proc.communicate()
    if stderr:
        for line in stderr:
            log.error(line)
        return False
    if proc.returncode != 0:
        log.error('Exit code not 0: {0}\n'.format(proc.returncode))
        return False
    return True

# run
conf = dict()
get_config(args)
log = configure_logging()

opsgenie_heartbeat_up = prometheus_client.Gauge('opsgenie_heartbeat_up', 'opsgenie heartbeat scrape status')
opsgenie_heartbeat_errors_total = prometheus_client.Counter('opsgenie_heartbeat_errors_total', 'heartbeat scrape errors total counter')

class Collector(object):
    def collect(self):
        # add static metrics
        try:
            if get_data():
                metric = prometheus_client.core.GaugeMetricFamily('opsgenie_heartbeat_prometheus_status', 'Status of prometheus check OK = 1', value=1)
            else:
                metric = prometheus_client.core.GaugeMetricFamily('opsgenie_heartbeat_prometheus_status', 'Status of prometheus check OK = 1', value=0)
            yield metric
            opsgenie_heartbeat_up.set(1)
        except:
            trace = traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
            for line in trace:
                log.error(line[:-1])
            opsgenie_heartbeat_up.set(0)
            opsgenie_heartbeat_errors_total.inc()

registry = prometheus_client.core.REGISTRY
registry.register(Collector())

prometheus_client.start_http_server(conf['listen_port'])

# endless loop
while True:
    try:
        while True:
            time.sleep(conf['check_interval'])
    except KeyboardInterrupt:
        break
    except:
        trace = traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
        for line in trace:
            log.error(line[:-1])

