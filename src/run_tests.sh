coverage run -m unittest discover -p '*test*.py' -s /src/
# coverage run -m unittest discover -p '*test*.py' .
# coverage html -d "./coverage"
coverage xml -o '/home/ubuntu/coverage/coverage.xml'