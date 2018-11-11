import requests
import os
import json

go_server = 'http://GOSERVER'


def get_environments():
    environments_api = '/go/api/admin/environments'

    accept = 'application/vnd.go.cd.v2+json'
    headers = {'Accept': accept}

    res = requests.get(go_server + environments_api, headers=headers)
    environments = res.json()['_embedded']['environments']

    if not os.path.exists('environments'):
        os.mkdir('environments')

    for environment in environments:
        environment_name = environment['name']
        environment_path = os.path.join('environments', environment_name)
        if not os.path.exists(environment_path):
            os.mkdir(os.path.join('environments', environment_name))

        for pipeline in environment['pipelines']:
            get_pipeline(environment_path, pipeline['name'])


def get_pipeline(environment_path, pipeline_name):
    pipelines_api = '/go/api/admin/pipelines/{pipeline_name}'

    accept = 'application/vnd.go.cd.v6+json'
    headers = {'Accept': accept}

    res = requests.get(go_server + pipelines_api.format(pipeline_name=pipeline_name), headers=headers)
    pipeline = res.json()

    with open(os.path.join(environment_path, pipeline_name+'.json'), 'w') as pipeline_file:
        json.dump(pipeline, pipeline_file, indent=4)


def get_templates():
    templates_api = '/go/api/admin/templates'

    accept = 'application/vnd.go.cd.v4+json'
    headers = {'Accept': accept}

    res = requests.get(go_server + templates_api, headers=headers)
    templates = res.json()['_embedded']['templates']

    templates_path = 'templates'

    if not os.path.exists(templates_path):
        os.mkdir(templates_path)

    for template in templates:
        get_template(templates_path, template['name'])


def get_template(templates_path, template_name):
    template_api = '/go/api/admin/templates/{template_name}'

    accept = 'application/vnd.go.cd.v4+json'
    headers = {'Accept': accept}

    res = requests.get(go_server + template_api.format(template_name=template_name), headers=headers)
    template = res.json()

    with open(os.path.join(templates_path, template['name']+'.json'), 'w') as template_file:
        json.dump(template, template_file, indent=4)


get_templates()

