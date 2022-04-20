import yaml

with open("discord_messages.yml", "r") as stream:
    discord_messages = yaml.safe_load(stream)

# Parse header sections for pipeline yaml
def parse_headers(pipeline, indent=0):
    line = ""
    if (type(pipeline) == dict):
        for item, doc in pipeline.items():
            for _ in range(0, indent):
                line += '\t'

            if (item == True):
                item = 'on'

            if (item == 'cron'):
                line += f"- {item}: "
            else:
                line += f"{item}: "

            if (type(doc) != dict and type(doc) != list):
                if (item == 'cron'):
                    line += f"\'{doc}\'\n"
                else:
                    line += f"{doc}\n"
            else:
                if (type(doc) == list):
                    if (type(doc[0]) != dict):
                        for branch in doc:
                            line += "\n"
                            for _ in range(indent):
                                line += "\t"
                            line += f"\t- \'{branch}\'\n"
                        continue
                    else:
                        doc = doc[0]
                line += "\n"
                line += parse_headers(doc, indent=indent+1) 
    else:
        print(pipeline)
        if (type(pipeline) == list):
            for itm in pipeline:
                for _ in range(0, indent):
                    line += '\t'
                line += f" - \'{itm}\'\n"
        line += "\n"

    line = line.replace('\t', ' ')
    return line

# Parse functionality yaml files for pipeline yaml
def parse_functions(pipeline, indent=2):
    line = ""
    if (type(pipeline) == dict):
        for item, doc in pipeline.items():

            for _ in range(indent):
                line += "\t"

            if "name" == item:
                line += f"- {item}: "
            else:
                line += f"\t{item}: "

            if (type(doc) != dict):
                if (item == "run"):
                    run_items = doc.split('\n')
                    if (len(run_items) > 1):
                        for run_itm in run_items:
                            if (run_itm == ''): 
                                line += "\n"
                                continue

                            line += " |\n"
                            for _ in range(indent):
                                line += "\t"
                            line += f"\t\t{run_itm}"
                    else:
                        line += f"{doc}\n"
                else:
                    line += f"{doc}\n"
            else:
                line += "\n"
                line += parse_functions(doc, indent=indent+1)

    line = line.replace('\t', ' ')
    return line

# Parse steps (functionality combination) for pipeline yaml
def parse_steps(steps):
    lines = []
    skip_message = False
    for j in range(len(steps)):
        if (skip_message):
            skip_message = False
            continue

        s = steps[j]

        file = f"pipeline_functions/{s}.yml"
        with open(file, "r") as stream:
            pipeline = yaml.safe_load(stream)

        if "discord_notifier" == s:
            pipeline[0]["with"]["args"] = discord_messages[steps[j+1]]
            skip_message = True
        
        line = ""
        for i in range(len(pipeline)):
            line += parse_functions(pipeline[i], indent=3)
            line += "\n"
        
        lines.append(line)

    return lines
