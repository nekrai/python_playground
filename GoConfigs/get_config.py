import requests
import os
import json

go_server = 'http://localhost:8153'
json_indent = 2


def get_environment(environment_path, environment_name):
    environment_api = '/go/api/admin/environments/{environment_name}'

    accept = 'application/vnd.go.cd.v2+json'
    headers = {'Accept': accept}

    res = requests.get(go_server + environment_api.format(environment_name=environment_name), headers=headers)
    environment = res.json()
    del environment['pipelines']
    del environment['_links']
    del environment['agents']

    with open(os.path.join(environment_path, environment_name+'.json'), 'w') as environment_file:
        json.dump(environment, environment_file, indent=json_indent)

    with open(os.path.join(environment_path, environment_name + '.etag'), 'w') as environment_etag_file:
        json.dump(res.headers['etag'], environment_etag_file)


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

        get_environment(environment_path, environment_name)

        for pipeline in environment['pipelines']:
            get_pipeline(environment_path, pipeline['name'])


def get_pipeline(environment_path, pipeline_name):
    pipelines_api = '/go/api/admin/pipelines/{pipeline_name}'

    accept = 'application/vnd.go.cd.v6+json'
    headers = {'Accept': accept}

    res = requests.get(go_server + pipelines_api.format(pipeline_name=pipeline_name), headers=headers)
    pipeline = res.json()
    del pipeline['origin']
    del pipeline['_links']

    pipeline_path = os.path.join(environment_path, pipeline_name)

    if not os.path.exists(pipeline_path):
        os.mkdir(pipeline_path)

    with open(os.path.join(pipeline_path, pipeline_name+'.json'), 'w') as pipeline_file:
        json.dump(pipeline, pipeline_file, indent=json_indent)

    with open(os.path.join(pipeline_path, pipeline_name+'.etag'), 'w') as pipeline_etag_file:
        json.dump(res.headers['etag'], pipeline_etag_file, indent=json_indent)


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
    del template['_links']

    template_path = os.path.join(templates_path, template_name)

    if not os.path.exists(template_path):
        os.mkdir(template_path)

    with open(os.path.join(template_path, template_name+'.json'), 'w') as template_file:
        json.dump(template, template_file, indent=json_indent)

    with open(os.path.join(template_path, template_name+'.etag'), 'w') as pipeline_etag_file:
        json.dump(res.headers['etag'], pipeline_etag_file, indent=json_indent)


if __name__ == '__main__':
    get_environments()
    get_templates()
