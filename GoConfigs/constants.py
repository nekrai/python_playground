go_server = 'http://localhost:8153'

environments_api = '/go/api/admin/environments'
environment_api = environments_api + '/{environment_name}'

environment_get_accept = 'application/vnd.go.cd.v2+json'
environment_get_headers = {'Accept': environment_get_accept}

environment_patch_accept = 'application/vnd.go.cd.v2+json'
environment_patch_headers = {
    'Accept': environment_patch_accept,
    'Content-Type': 'application/json'
}

environment_post_accept = 'application/vnd.go.cd.v2+json'
environment_post_headers = {
    'Accept': environment_post_accept,
    'Content-Type': 'application/json'
}

environment_delete_accept = 'application/vnd.go.cd.v2+json'
environment_delete_headers = {
    'Accept': environment_delete_accept,
    'Content-Type': 'application/json'
}

pipelines_api = '/go/api/admin/pipelines'
pipeline_api = pipelines_api + '/{pipeline_name}'

pipeline_get_accept = 'application/vnd.go.cd.v6+json'
pipeline_get_headers = {'Accept': pipeline_get_accept}

pipeline_put_accept = 'application/vnd.go.cd.v6+json'
pipeline_put_headers = {
        'Accept': pipeline_put_accept,
        'Content-Type': 'application/json'
}

pipeline_post_accept = 'application/vnd.go.cd.v6+json'
pipeline_post_headers = {
        'Accept': pipeline_post_accept,
        'Content-Type': 'application/json'
}

pipeline_delete_accept = 'application/vnd.go.cd.v6+json'
pipeline_delete_headers = {'Accept': pipeline_get_accept}

templates_api = '/go/api/admin/templates'
template_api = templates_api + '/{template_name}'

template_get_accept = 'application/vnd.go.cd.v4+json'
template_get_headers = {'Accept': template_get_accept}

template_put_accept = 'application/vnd.go.cd.v4+json'
template_put_headers = {
    'Accept': template_put_accept,
    'Content-Type': 'application/json'
}

template_post_accept = 'application/vnd.go.cd.v4+json'
template_post_headers = {
    'Accept': template_post_accept,
    'Content-Type': 'application/json'
}

template_delete_accept = 'application/vnd.go.cd.v4+json'
template_delete_headers = {'Accept': template_delete_accept}
