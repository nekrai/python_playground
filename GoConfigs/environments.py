import requests
import os
import json
from get_config import get_environment
from variables import restore_variables_in
from constants import environments_api, environment_headers


def get_etag(environment_name):
    res = requests.get(environments_api + environment_name, headers=environment_headers['get'])
    if res.status_code != 200:
        raise Exception('Could not get etag for environment ' + environment_name)

    return res.headers['etag']


def get_environment_variables(environment_name):
    res = requests.get(environments_api + environment_name, headers=environment_headers['get'])
    if res.status_code != 200:
        raise Exception('Could not get environment ' + environment_name)

    environment = res.json()
    return [var['name'] for var in environment['environment_variables']]


def validate_etag(environment_name):
    etag = get_etag(environment_name)

    environment_path = os.path.join('environments', environment_name)

    with open(os.path.join(environment_path, environment_name + '.etag'), 'r') as environment_etag_file:
        environment_etag = json.load(environment_etag_file)

    if etag != environment_etag:
        print 'Conflict detected! Environment ' + environment_name + ' was changed via UI!'
        print 'Update your local copy!'
        raise Exception('Local etag is different than server etag')


def read_and_restore_environment(environment_path, environment_name):
    with open(os.path.join(environment_path, environment_name + '.json'), 'r') as environment_file:
        environment = json.load(environment_file)

    restore_variables_in(environment)

    return environment


def update_environment(environment_name):
    environment_path = os.path.join('environments', environment_name)
    environment = read_and_restore_environment(environment_path, environment_name)

    environment_variables_add = {
        "environment_variables": {
            "add": environment['environment_variables'],
            "remove": get_environment_variables(environment_name)
        }
    }

    validate_etag(environment_name)

    res = requests.patch(environments_api + environment_name, data=json.dumps(environment_variables_add), headers=environment_headers['patch'])
    if res.status_code == 200:
        print 'Environment {} updated successfully. Refreshing ETag.'.format(environment_name)
        get_environment(environment_path, environment_name)
    else:
        print res, res.text


def create_environment(environment_name):
    environment_path = os.path.join('environments', environment_name)

    if not os.path.exists(environment_path):
        raise Exception('Environment configuration not found!')

    environment = read_and_restore_environment(environment_path, environment_name)

    res = requests.post(environments_api, data=json.dumps(environment), headers=environment_headers['post'])
    if res.status_code == 200:
        print 'Environment {} created successfully. Refreshing ETag.'.format(environment_name)
        get_environment(environment_path, environment_name)
    else:
        print res, res.text


def delete_environment(environment_name):
    res = requests.delete(environments_api + environment_name, headers=environment_headers['del'])
    if res.status_code == 200:
        print 'Environment {} deleted successfully.'.format(environment_name)
    else:
        print res, res.text


def add_pipeline_to_environment(environment_name, pipeline_name):
    _pipeline_operation_in_environment('add', environment_name, pipeline_name)


def remove_pipeline_from_environment(environment_name, pipeline_name):
    _pipeline_operation_in_environment('remove', environment_name, pipeline_name)


_operations = {
    'add': 'added',
    'remove': 'removed'
}


def _pipeline_operation_in_environment(operation, environment_name, pipeline_name):
    pipelines_op = {
        "pipelines": {
            operation: [pipeline_name]
        }
    }

    res = requests.patch(environments_api + environment_name, data=json.dumps(pipelines_op), headers=environment_headers['patch'])
    if res.status_code == 200:
        print 'Pipeline {pipeline_name} {operation} to environment {environment_name}. Refreshing ETag.'\
            .format(operation=_operations[operation], pipeline_name=pipeline_name, environment_name=environment_name)
        environment_path = os.path.join('environments', environment_name)
        get_environment(environment_path, environment_name)
    else:
        print res, res.text


if __name__ == '__main__':
    update_environment('ExampleEnv')
    create_environment('NewEnv')
    delete_environment('NewEnv')
