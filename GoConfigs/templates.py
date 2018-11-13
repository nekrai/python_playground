import requests
import os
import json
from get_config import get_template
from constants import go_server, template_api, templates_api, template_get_headers, template_post_headers, template_put_headers, template_delete_headers


def get_etag(template_name):
    res = requests.get(go_server + template_api.format(template_name=template_name), headers=template_get_headers)
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


def update_template(template_name):
    template_path = os.path.join('templates', template_name)

    with open(os.path.join(template_path, template_name + '.json'), 'r') as template_file:
        template = json.load(template_file)

    template_put_headers['If-Match'] = validate_etag(template_name)
    res = requests.put(go_server + template_api.format(template_name=template_name), data=json.dumps(template), headers=template_put_headers)

    if res.status_code == 200:
        print 'Template ' + template_name + ' updated successfully. Refreshing ETag.'
        get_template('templates', template_name)
    else:
        print res.text


def create_template(template_name):
    template_path = os.path.join('templates', template_name)

    with open(os.path.join(template_path, template_name + '.json'), 'r') as template_file:
        template = json.load(template_file)

    res = requests.post(go_server + templates_api, data=json.dumps(template), headers=template_post_headers)
    print res

    if res.status_code == 200:
        print 'Template ' + template_name + ' created successfully. Refreshing ETag.'
        get_template('templates', template_name)
    else:
        print res.text


def delete_template(template_name):
    res = requests.delete(go_server + template_api.format(template_name=template_name), headers=template_delete_headers)
    print res

    if res.status_code == 200:
        print 'Template ' + template_name + ' deleted successfully.'
    else:
        print res.text


create_template('AnotherTemplate')
