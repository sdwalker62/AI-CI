#!/usr/bin/env python

import pip
import os
import subprocess
from subprocess import CalledProcessError, PIPE
import functools
import logging


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package]) 
        
run = functools.partial(subprocess.run, shell=True)

def run_cmd(cmd):
  return subprocess.run(
    cmd, 
    shell=True, 
    stdout=PIPE, 
    stderr=PIPE, 
    check=True).stdout.decode('utf-8')
        
        
# Imports
import_or_install('docker')


font_colors = {
    'green': '\033[0;32m',
    'blue': '\033[1;34m',
    'clear': '\033[0m'
}


def check_mark():
    logging.info(f"{font_colors['green']} \u2714 {font_colors['clear']}")


logging.info(f"{font_colors['blue']} =================== {font_colors['clear']}")
logging.info(f"{font_colors['blue']} RUNNING CI PIPELINE {font_colors['clear']}")
logging.info(f"{font_colors['blue']} =================== {font_colors['clear']}")

if os.path.isfile('./Dockerfile.ci'):
    import docker
    logging.info('Acquiring docker client ... ')
    # client = docker.from_env()
    api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
    client = docker.from_env()
    check_mark()
    
    # IMAGE BUILDER
    # ====================================================== #
    logging.info('******************************')
    logging.info('Building CI Image ... ')
    builder = api_client.build(
        path='.', 
        dockerfile='Dockerfile.ci',
        tag='ai_ci',
        decode=True
    )
    for chunk in builder:
        if 'stream' in chunk:
            for line in chunk['stream'].splitlines():
                logging.info(line)
    logging.info('******************************')
    check_mark()
    # ====================================================== #
    
    
    # RUN CONTAINER
    # ======================================================
    logging.info('Executing pipeline ... ')
    pwd = run_cmd("pwd").replace('\n', '')
    ci_container = client.containers.run(
        image='ai_ci', 
        detach=True,
        volumes=[f'{pwd}/.github/workflows:/home/ubuntu/coverage']
    )
    process = ci_container.logs(stream=True, follow=True)
    for line in process:
        logging.info(line.decode('utf-8').replace('\n', ''))
    
    check_mark()
else:
    logging.warn('No Dockerfile found!')
    
