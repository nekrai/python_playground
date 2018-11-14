json_indent = 2

go_server = 'http://localhost:8153'

versions = {
    'v2': 'application/vnd.go.cd.v2+json',
    'v4': 'application/vnd.go.cd.v4+json',
    'v6': 'application/vnd.go.cd.v6+json'
}

environments_api = go_server + '/go/api/admin/environments/'
pipelines_api = go_server + '/go/api/admin/pipelines/'
templates_api = go_server + '/go/api/admin/templates/'


def _headers(version):
    return {
        'get': {
            'Accept': versions[version]
        },
        'patch': {
            'Accept': versions[version],
            'Content-Type': 'application/json'
        },
        'put': {
            'Accept': versions[version],
            'Content-Type': 'application/json'
        },
        'post': {
            'Accept': versions[version],
            'Content-Type': 'application/json'
        },
        'del': {
            'Accept': versions[version]
        },
    }


environment_headers = _headers('v2')
pipeline_headers = _headers('v6')
template_headers = _headers('v4')
