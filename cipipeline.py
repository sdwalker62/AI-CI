#!/usr/bin/env python

import pip
import os
import subprocess
from subprocess import CalledProcessError, PIPE
import functools


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


print('=========================')
print(f"{font_colors['blue']} RUNNING CI PIPELINE {font_colors['clear']}")
print('=========================')

if os.path.isfile('./Dockerfile.ci'):
    import docker
    client = docker.from_env()
    client.images.build(
        path='.', 
        dockerfile='Dockerfile.ci',
        tag='ai_ci'
    )
    client.containers.run(image='ai_ci')
    scp_cmd = 'scp -i "sonarqube.pem" coverage/index.html ubuntu@ec2-44-196-133-163.compute-1.amazonaws.com:/var/www/html/'
    run_cmd(scp_cmd)
    
