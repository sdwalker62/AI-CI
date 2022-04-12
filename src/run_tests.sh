coverage run -m unittest discover -p '*test*.py' ./unittests/
# coverage html -d "./coverage"
coverage xml -o './coverage/coverage.xml'