import requests

ServerURL = 'http://localhost:8153'
PipelineName = 'Another'

PipelineAPI = ServerURL + '/go/api/admin/pipelines/{0}'

Accept = 'application/vnd.go.cd.v3+json'
headers = {'Accept': Accept}

res = requests.get(PipelineAPI.format(PipelineName), headers=headers)

not_supported = [
    '_links',
    'run_instance_count',
    'parameters',
    'submodule_folder',
    'shallow_clone',
    'invert_filter',
    'template',
    'authorization',
    'timeout'
]


def supported(key):
    return key not in not_supported


def transform_json(json_elem):
    transformed = {}
    for key in json_elem.keys():
        if supported(key):
            inner_transformed = transform_config(json_elem[key])
            if inner_transformed is None:
                continue
            elif key == 'attributes':
                transformed.update(inner_transformed)
            elif key == 'run_if':
                if len(inner_transformed) != 0:
                    transformed[str(key)] = inner_transformed[0]
            elif key == 'properties':
                transformed[str(key)] = [inner_transformed]
            else:
                transformed[str(key)] = inner_transformed

    return transformed


def transform_list(list_elem):
    transformed = []
    for elem in list_elem:
        transformed.append(transform_config(elem))
    return transformed


def transform_config(element):
    if isinstance(element, dict):
        return transform_json(element)

    if isinstance(element, list):
        return transform_list(element)

    if element == str(element):
       return str(element)

    return element

the_json = res.json()
print the_json
the_json['group'] = 'bah'
the_json['name'] = 'Test2'

transformed = transform_config(the_json)

def print_json(json_elem):
    print "{"
    keys = json_elem.keys()
    if len(keys) != 0:
        for key in keys[:-1]:
            print '"{}":'.format(key)
            print_elem(json_elem[key])
            print ","
        print '"{}":'.format(keys[-1])
        print_elem(json_elem[keys[-1]])
    print "}"


def print_list(list_elem):
    print "["
    if len(list_elem) != 0:
        for elem in list_elem[:-1]:
            print_elem(elem)
            print ","
        print_elem(list_elem[-1])
    print "]"


def print_elem(element):
    if isinstance(element, dict):
        print_json(element)

    if isinstance(element, list):
        print_list(element)

    if element == str(element):
        print '"{}"'.format(str(element))

    if element is None:
        print "null"

    if element is False:
        print "false"

    if element is True:
        print "true"


print_elem(transformed)
