coverage run -m unittest discover -p '*test*.py' ./unittests/
# coverage html -d "./coverage"
coverage xml -o './coverage/coverage.xml'

scp -i "sonarqube.pem" ./coverage/coverage.xml ubuntu@ec2-44-196-133-163.compute-1.amazonaws.com:~/sonarqube