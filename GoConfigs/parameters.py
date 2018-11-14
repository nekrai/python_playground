parameters = {
    "Par1": "bulbasaur",
    "Par2": "lolz"
}


def replace_parameters_in(config):
    for par in config['parameters']:
        if par['name'] in parameters and par['value'] == parameters[par['name']]:
            par['value'] = '[REPLACED]'


def restore_parameters_in(config):
    for par in config['parameters']:
        if par['value'] == '[REPLACED]':
            par['value'] = parameters[par['name']]
