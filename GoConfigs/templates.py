import requests
import os
import json
from get_config import get_template
from constants import templates_api, template_headers
from variables import restore_variables_in


def get_etag(template_name):
    res = requests.get(templates_api + template_name, headers=template_headers['get'])
    if res.status_code != 200:
        raise Exception('Could not get etag for template ' + template_name)

    return res.headers['etag']


def validate_etag(template_name):
    etag = get_etag(template_name)

    with open(os.path.join('templates', template_name, template_name + '.etag'), 'r') as template_etag_file:
        template_etag = json.load(template_etag_file)

    if etag != template_etag:
        print 'Conflict detected! Template ' + template_name + ' was changed via UI!'
        print 'Update your working copy!'
        raise Exception('Local etag is different than server etag')

    return etag


def read_and_restore(template_path, template_name):
    with open(os.path.join(template_path, template_name + '.json'), 'r') as template_file:
        template = json.load(template_file)

    for stage in template['stages']:
        restore_variables_in(stage)

        for job in stage['jobs']:
            restore_variables_in(job)

    return template


def update_template(template_name):
    template_path = os.path.join('templates', template_name)
    template = read_and_restore(template_path, template_name)
    template_headers['put']['If-Match'] = validate_etag(template_name)

    res = requests.put(templates_api + template_name, data=json.dumps(template), headers=template_headers['put'])
    if res.status_code == 200:
        print 'Template ' + template_name + ' updated successfully. Refreshing ETag.'
        get_template(template_name)
    else:
        print res, res.text


def create_template(template_name):
    template_path = os.path.join('templates', template_name)
    template = read_and_restore(template_path, template_name)

    res = requests.post(templates_api, data=json.dumps(template), headers=template_headers['post'])
    if res.status_code == 200:
        print 'Template ' + template_name + ' created successfully. Refreshing ETag.'
        get_template(template_name)
    else:
        print res, res.text


def delete_template(template_name):
    res = requests.delete(templates_api + template_name, headers=template_headers['del'])

    if res.status_code == 200:
        print 'Template ' + template_name + ' deleted successfully.'
    else:
        print res, res.text


if __name__ == '__main__':
    update_template('TempTemp')
    create_template('NewTemplate')
    delete_template('NewTemplate')
