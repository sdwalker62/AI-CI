#!/bin/bash


# Color variables
green='\033[0;32m'
blue='\033[1;34m'
clear='\033[0m'


echo "${blue}======================${clear}"
echo "${blue}RUNNING AI CI PIPELINE${clear}"
echo "${blue}======================${clear}"


if [[ -f "./Dockerfile.ci" ]]; then
    docker build -t ci_pipeline -f Dockerfile.ci .
    docker run -v `pwd`/coverage/:/coverage/ ci_pipeline
    scp -i "sonarqube.pem" coverage/converage.xml ubuntu@ec2-44-196-133-163.compute-1.amazonaws.com:/home/ubuntu/sonarqube/conf/
    echo "${green}FINISH${clear}"
else
    echo "No Dockerfile found!"
fi 
