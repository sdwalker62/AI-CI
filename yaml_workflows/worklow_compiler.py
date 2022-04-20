#!/usr/bin/env python

from ruamel.yaml import YAML
from workflow_parsers import parse_steps
from pipeline_steps import commit_steps, merge_steps, pr_nightly_steps

file = {}

yaml = YAML()
    
with open("workflow_headers.yml", "r") as stream:
    file = yaml.load(stream)

pipeline_files = ["commit-pipeline", "merge-pipeline", "pr_nightly-pipeline"]

print("Enter Build Options:\n\t")
print(" - commit-pipeline\n\t")
print(" - merge-pipeline\n\t")
print(" - pr_nightly-pipeline\n\t")
print(" - all-pipelines\n\t")

x = input()

steps = []

while x not in file and x != "all-pipelines":
    print("Invalid option...\n")
    x = input()

if "commit-pipeline" == x:
    steps = [commit_steps]
    x = [0]
elif "merge-pipeline" == x:
    steps = [merge_steps]
    x = [1]
elif "pr_nightly-pipeline" == x:
    steps = [pr_nightly_steps]
    x = [2]
else:
    steps = [commit_steps, merge_steps, pr_nightly_steps]
    x = [0, 1, 2]

for i in range(0, len(steps)):
    p = pipeline_files[x[i]]

    workflow = open(f'../.github/workflows/{p}.yaml', 'w')

    workflow_pipeline = file[p]

    step_documents = parse_steps(steps[i])
    
    if "jobs" in workflow_pipeline:
        keyList = list(workflow_pipeline['jobs'].keys())
        workflow_pipeline['jobs'][keyList[0]]['steps'] = step_documents['steps']

    # Write compiled yaml file
    documents = yaml.dump(workflow_pipeline, workflow)

    # Close File
    workflow.close()