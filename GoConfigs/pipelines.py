import requests
import os
import json
from get_config import get_pipeline
from environments import add_pipeline_to_environment, remove_pipeline_from_environment
from constants import go_server, pipelines_api, pipeline_api, pipeline_delete_headers, pipeline_get_headers, pipeline_post_headers, pipeline_put_headers


def get_etag(pipeline_name):
    res = requests.get(go_server + pipeline_api.format(pipeline_name=pipeline_name), headers=pipeline_get_headers)
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


def update_pipeline(pipeline_name):
    environment_path = os.path.join('environments', 'ExampleEnv')

    with open(os.path.join(environment_path, pipeline_name, pipeline_name + '.json'), 'r') as pipeline_file:
        pipeline = json.load(pipeline_file)

    pipeline_put_headers['If-Match'] = validate_etag(environment_path, pipeline_name)

    res = requests.put(go_server + pipeline_api.format(pipeline_name=pipeline_name), data=json.dumps(pipeline), headers=pipeline_put_headers)

    if res.status_code == 200:
        print 'Pipeline {} updated successfully. Refreshing ETag.'.format(pipeline_name)
        get_pipeline(environment_path, pipeline_name)
    else:
        print res.text


def create_pipeline(environment_name, pipeline_name):
    environment_path = os.path.join('environments', environment_name)

    with open(os.path.join(environment_path, pipeline_name, pipeline_name + '.json'), 'r') as pipeline_file:
        pipeline = json.load(pipeline_file)

    pipeline_group = {
        'group': environment_name,
        'pipeline': pipeline
    }

    res = requests.post(go_server + pipelines_api, data=json.dumps(pipeline_group), headers=pipeline_post_headers)

    if res.status_code == 200:
        print 'Pipeline {} created successfully. Refreshing ETag.'.format(pipeline_name)
        get_pipeline(environment_path, pipeline_name)
        print 'Adding pipeline {} to environment {}.'.format(pipeline_name, environment_name)
        add_pipeline_to_environment(environment_name, pipeline_name)
    else:
        print res.text


def delete_pipeline(environment_name, pipeline_name):
    remove_pipeline_from_environment(environment_name, pipeline_name)

    res = requests.delete(go_server + pipeline_api.format(pipeline_name=pipeline_name), headers=pipeline_delete_headers)
    print res
    if res.status_code == 200:
        print 'Pipeline ' + pipeline_name + ' removed successfully.'
    else:
        print res.text


if __name__ == '__main__':
    delete_pipeline('ExampleEnv', 'Pires')
