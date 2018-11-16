import json

with open('parameters.json') as p:
    parameters = json.load(p)


def replace_parameters_in(config):
    for par in config['parameters']:
        if par['name'] in parameters and par['value'] in parameters[par['name']]:
            par['value'] = '[REPLACED BY VALUE {}]'.format(parameters[par['name']].index(par['value']))


def restore_parameters_in(config):
    for par in config['parameters']:
        if par['value'].startswith('[REPLACED BY VALUE'):
            pos = int(par['value'][len('[REPLACED BY VALUE '):-len(']')])
            par['value'] = parameters[par['name']][pos]
