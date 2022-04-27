from ruamel.yaml import YAML

yaml = YAML()

with open("discord_messages.yml", "r") as stream:
    discord_messages = yaml.load(stream)

# Parse steps (functionality combination) for pipeline yaml
def parse_steps(steps):
    step_dict = {'steps': []}

    skip_message = False
    for j in range(len(steps)):
        if (skip_message):
            skip_message = False
            continue

        s = steps[j]

        file = f"./pipeline_functions/{s}.yml"
        with open(file, "r") as stream:
            pipeline = yaml.load(stream)

        if "discord_notifier" == s:
            pipeline[0]["with"]["args"] = discord_messages[steps[j+1]]
            skip_message = True

        for i in range(len(pipeline)):
            step_dict['steps'].append(pipeline[i])

    return step_dict
