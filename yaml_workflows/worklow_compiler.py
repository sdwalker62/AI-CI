#!/usr/bin/env python

import yaml
from workflow_parsers import parse_headers, parse_steps
from pipeline_steps import commit_steps, merge_steps, pr_nightly_steps

file = {}


with open("discord_messages.yml", "r") as stream:
    discord_messages = yaml.safe_load(stream)
    
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

    workflow_pipeline = file[p]

    # documents = yaml.dump(pipeline, workflow)

    step_dict = {'steps': []}

    skip_message = False
    for j in range(len(steps[i])):
        if (skip_message):
            skip_message = False
            continue

        s = steps[i][j]
        print(s)

        file = f"./pipeline_functions/{s}.yml"
        with open(file, "r") as stream:
            pipeline = yaml.safe_load(stream)

        if "discord_notifier" == s:
            pipeline[0]["with"]["args"] = discord_messages[steps[i][j+1]]
            skip_message = True

        step_dict['steps'].append(pipeline[0])
    
    print(workflow_pipeline)
    if "jobs" in workflow_pipeline:
        print(workflow_pipeline.keys())
        keyList = list(workflow_pipeline['jobs'].keys())
        workflow_pipeline['jobs'][keyList[0]]['steps'] = step_dict['steps']

    documents = yaml.dump(workflow_pipeline, workflow)
        


    # Headers
    # workflow.writelines(parse_headers(pipeline))

    # # Steps
    # workflow.writelines(parse_steps(steps[i]))

    # Close File
    workflow.close()