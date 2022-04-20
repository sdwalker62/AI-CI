#!/usr/bin/env python

import yaml
from workflow_parsers import parse_headers, parse_steps
from pipeline_steps import commit_steps, merge_steps, pr_nightly_steps

file = {}

with open("workflow_headers.yml", "r") as stream:
    file = yaml.safe_load(stream)

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

print(steps)
print(x)

for i in range(0, len(steps)):
    p = pipeline_files[x[i]]
    print(p)

    workflow = open(f'../.github/workflows/{p}.yaml', 'w')

    pipeline = file[p]

    # Headers
    workflow.writelines(parse_headers(pipeline))

    # Steps Header
    workflow.writelines("    steps:\n")

    # Steps
    workflow.writelines(parse_steps(steps[i]))

    # Close File
    workflow.close()