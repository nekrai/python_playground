import requests
import os
import json

from get_config import get_pipeline
from environments import add_pipeline_to_environment, remove_pipeline_from_environment
from constants import pipelines_api, pipeline_headers
from repositories import restore_repositories_in_pipeline
from variables import restore_variables_in
from parameters import restore_parameters_in


def get_etag(pipeline_name):
    res = requests.get(pipelines_api + pipeline_name, headers=pipeline_headers['get'])
    if res.status_code != 200:
        raise Exception('Could not get etag for pipeline ' + pipeline_name)

    return res.headers['etag']


def validate_etag(environment_path, pipeline_name):
    etag = get_etag(pipeline_name)

    with open(os.path.join(environment_path, pipeline_name, pipeline_name + '.etag'), 'r') as pipeline_etag_file:
        pipeline_etag = json.load(pipeline_etag_file)

    if etag != pipeline_etag:
        print 'Conflict detected! Pipeline ' + pipeline_name + ' was changed via UI!'
        print 'Update your local copy!'
        raise Exception('Local etag is different than server etag')

    return etag


def read_and_restore_pipeline(environment_path, pipeline_name):
    with open(os.path.join(environment_path, pipeline_name, pipeline_name + '.json'), 'r') as pipeline_file:
        pipeline = json.load(pipeline_file)

    restore_repositories_in_pipeline(pipeline)
    restore_variables_in(pipeline)
    restore_parameters_in(pipeline)

    return pipeline


def update_pipeline(environment_name, pipeline_name):
    environment_path = os.path.join('environments', environment_name)
    pipeline = read_and_restore_pipeline(environment_path, pipeline_name)
    pipeline_headers['put']['If-Match'] = validate_etag(environment_path, pipeline_name)

    res = requests.put(pipelines_api + pipeline_name, data=json.dumps(pipeline), headers=pipeline_headers['put'])
    if res.status_code == 200:
        print 'Pipeline {} updated successfully. Refreshing ETag.'.format(pipeline_name)
        get_pipeline(environment_path, pipeline_name)
    else:
        print res, res.text


def create_pipeline(environment_name, pipeline_name):
    environment_path = os.path.join('environments', environment_name)
    pipeline = read_and_restore_pipeline(environment_path, pipeline_name)
    pipeline_group = {
        'group': environment_name,
        'pipeline': pipeline
    }

    res = requests.post(pipelines_api, data=json.dumps(pipeline_group), headers=pipeline_headers['post'])
    if res.status_code == 200:
        print 'Pipeline {} created successfully. Refreshing ETag.'.format(pipeline_name)
        get_pipeline(environment_path, pipeline_name)
        print 'Adding pipeline {} to environment {}.'.format(pipeline_name, environment_name)
        add_pipeline_to_environment(environment_name, pipeline_name)
    else:
        print res, res.text


def delete_pipeline(environment_name, pipeline_name):
    remove_pipeline_from_environment(environment_name, pipeline_name)

    res = requests.delete(pipelines_api + pipeline_name, headers=pipeline_headers['del'])
    if res.status_code == 200:
        print 'Pipeline {} deleted successfully.'.format(pipeline_name)
    else:
        print res, res.text


if __name__ == '__main__':
    update_pipeline('ExampleEnv', 'Mario')
    create_pipeline('ExampleEnv', 'Pires')
    delete_pipeline('ExampleEnv', 'Pires')

