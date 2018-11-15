import json

with open('variables.json') as v:
    variables = json.load(v)


def replace_variables_in(config):
    for var in config['environment_variables']:
        if var['name'] in variables and var['value'] == variables[var['name']]:
            var['value'] = '[REPLACED]'


def restore_variables_in(config):
    for var in config['environment_variables']:
        if var['value'] == '[REPLACED]':
            var['value'] = variables[var['name']]
