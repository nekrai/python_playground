import requests
import os
import json
from repositories import replace_repositories_in_pipeline
from variables import replace_variables_in
from parameters import replace_parameters_in
from constants import environments_api, pipelines_api, templates_api, \
    environment_headers, pipeline_headers, template_headers, json_indent


def get_environment(environment_path, environment_name):
    res = requests.get(environments_api + environment_name, headers=environment_headers['get'])
    environment = res.json()

    del environment['pipelines']
    del environment['_links']
    del environment['agents']

    replace_variables_in(environment)

    with open(os.path.join(environment_path, environment_name+'.json'), 'w') as environment_file:
        json.dump(environment, environment_file, indent=json_indent)

    with open(os.path.join(environment_path, environment_name + '.etag'), 'w') as environment_etag_file:
        json.dump(res.headers['etag'], environment_etag_file)


def get_environments():
    res = requests.get(environments_api, headers=environment_headers['get'])
    environments = res.json()['_embedded']['environments']

    if not os.path.exists('environments'):
        os.mkdir('environments')

    for environment in environments:
        environment_name = environment['name']
        environment_path = os.path.join('environments', environment_name)

        if not os.path.exists(environment_path):
            os.mkdir(os.path.join('environments', environment_name))

        get_environment(environment_path, environment_name)

        for pipeline in environment['pipelines']:
            get_pipeline(environment_path, pipeline['name'])


def get_pipeline(environment_path, pipeline_name):
    res = requests.get(pipelines_api + pipeline_name, headers=pipeline_headers['get'])
    pipeline = res.json()

    del pipeline['origin']
    del pipeline['_links']

    replace_repositories_in_pipeline(pipeline)
    replace_variables_in(pipeline)
    replace_parameters_in(pipeline)

    pipeline_path = os.path.join(environment_path, pipeline_name)

    if not os.path.exists(pipeline_path):
        os.mkdir(pipeline_path)

    with open(os.path.join(pipeline_path, pipeline_name+'.json'), 'w') as pipeline_file:
        json.dump(pipeline, pipeline_file, indent=json_indent)

    with open(os.path.join(pipeline_path, pipeline_name+'.etag'), 'w') as pipeline_etag_file:
        json.dump(res.headers['etag'], pipeline_etag_file, indent=json_indent)


def get_templates():
    res = requests.get(templates_api, headers=template_headers['get'])
    templates = res.json()['_embedded']['templates']

    if not os.path.exists('templates'):
        os.mkdir('templates')

    for template in templates:
        get_template(template['name'])


def get_template(template_name):
    res = requests.get(templates_api + template_name, headers=template_headers['get'])
    template = res.json()

    del template['_links']

    for stage in template['stages']:
        replace_variables_in(stage)

        for job in stage['jobs']:
            replace_variables_in(job)

    template_path = os.path.join('templates', template_name)

    if not os.path.exists(template_path):
        os.mkdir(template_path)

    with open(os.path.join(template_path, template_name+'.json'), 'w') as template_file:
        json.dump(template, template_file, indent=json_indent)

    with open(os.path.join(template_path, template_name+'.etag'), 'w') as pipeline_etag_file:
        json.dump(res.headers['etag'], pipeline_etag_file, indent=json_indent)


if __name__ == '__main__':
    get_environments()
    get_templates()
