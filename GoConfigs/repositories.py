import json

with open('repositories.json') as r:
    reps = json.load(r)
    repositories = reps['repositories']
    credentials = reps['credentials']
    credentials_users = [credential.keys()[0] for credential in credentials]


def _get_credentials_of_user(username):
    return [credential[username] for credential in credentials if username in credential][0]


def replace_repositories_in_pipeline(pipeline):
    for material in pipeline['materials']:
        _replace_urls(material)
        _replace_credentials(material)


def _replace_urls(material):
    urls = [
        url for url in repositories
        if repositories[url] == material['attributes']['url']
    ]
    if urls:
        material['attributes']['url'] = urls[0]
    else:
        print "Material URL not found! I'm not replacing it! " + material['attributes']['url']


def _replace_credentials(material):
    if 'username' in material['attributes']:
        if material['attributes']['username'] in credentials_users:
            user_passwords = _get_credentials_of_user(material['attributes']['username'])
            if material['attributes']['encrypted_password'] in user_passwords:
                material['attributes']['username'] = '[REPLACED BY VALUE {}]'.format(credentials_users.index(material['attributes']['username']))
                material['attributes']['encrypted_password'] = '[REPLACED BY VALUE {}]'.format(user_passwords.index(material['attributes']['encrypted_password']))
        else:
            print 'Username and password not replaced! ' + material['attributes']['username'] + ' ' + material['attributes']['encrypted_password']


def restore_repositories_in_pipeline(pipeline):
    for material in pipeline['materials']:
        _restore_urls(material)
        _restore_credentials(material)


def _restore_urls(material):
    if material['attributes']['url'] == '[REPLACED]':
        material['attributes']['url'] = repositories[material['attributes']['url']]


def _restore_credentials(material):
    if material['attributes']['username'].startswith('[REPLACED BY VALUE '):
        username_pos = int(material['attributes']['username'][len('[REPLACED BY VALUE '):-len(']')])
        username = credentials_users[username_pos]
        material['attributes']['username'] = username

        user_passwords = _get_credentials_of_user(username)

        password_pos = int(material['attributes']['encrypted_password'][len('[REPLACED BY VALUE '):-len(']')])
        material['attributes']['encrypted_password'] = user_passwords[password_pos]
