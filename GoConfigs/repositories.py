import json

with open('repositories.json') as r:
    reps = json.load(r)
    repositories = reps['repositories']
    credentials = reps['credentials']


def replace_repositories_in_pipeline(pipeline):
    for material in pipeline['materials']:
        urls = [
            url for url in repositories
            if repositories[url] == material['attributes']['url']
        ]
        if urls:
            material['attributes']['url'] = urls[0]
        else:
            print "Material URL not found! I'm not replacing it! " + material['attributes']['url']

        if 'username' in material['attributes']:
            if material['attributes']['username'] == credentials['username'] and material['attributes']['encrypted_password'] == credentials['encrypted_password']:
                material['attributes']['username'] = '[REPLACED]'
                material['attributes']['encrypted_password'] = '[REPLACED]'
            else:
                print 'Username and password not replaced! ' + material['attributes']['username'] + ' ' + material['attributes']['encrypted_password']


def restore_repositories_in_pipeline(pipeline):
    for material in pipeline['materials']:
        material['attributes']['url'] = repositories[material['attributes']['url']]
        material['attributes']['username'] = credentials['username']
        material['attributes']['encrypted_password'] = credentials['encrypted_password']
