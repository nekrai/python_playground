import json

with open('variables.json') as v:
    variables = json.load(v)


def replace_variables_in(config):
    for var in config['environment_variables']:
        if var['name'] in variables and var['value'] in variables[var['name']]:
            var['value'] = '[REPLACED BY VALUE {}]'.format(variables[var['name']].index(var['value']))


def restore_variables_in(config):
    for var in config['environment_variables']:
        if var['value'].startswith('[REPLACED BY VALUE'):
            pos = int(var['value'][len('[REPLACED BY VALUE '):-len(']')])
            var['value'] = variables[var['name']][pos]
