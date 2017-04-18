import logging

import salt.exceptions

import requests
from requests.compat import urljoin

LOG = logging.getLogger(__name__)


def get_project(name):
    session, make_url = get_session()
    resp = session.get(make_url("/api/18/project/{}".format(name)))
    status_code = resp.status_code
    if status_code == 200:
        return resp.json()
    elif status_code == 404:
        return None
    raise salt.exceptions.SaltInvocationError(
        "Could not retrieve information about project {} from Rundeck {}: {}"
        .format(name, make_url.base_url, status_code))


def create_project(name, params):
    session, make_url = get_session()
    config = create_project_config(name, params)
    LOG.debug("create_project: %s", name)
    LOG.warning("create_project.config: %s/%s", name, config)
    resp = session.post(
        make_url("/api/18/projects"),
        json={
            'name': name,
            'config': config,
        },
        allow_redirects=False,
    )
    if resp.status_code == 201:
        return resp.json()
    LOG.debug("create_project: %s", name)


def create_project_config(name, params, config=None):
    config = dict(config) if config else {}
    if params['description']:
       config['project.description'] = params['description']
    else:
       config.pop('project.description', None)
    config.update({
        'resources.source.1.config.file':
                "/var/rundeck/projects/{}/etc/resources.yaml".format(name),
        'resources.source.1.config.format': 'resourceyaml',
        'resources.source.1.config.generateFileAutomatically': 'true',
        'resources.source.1.config.includeServerNode': 'false',
        'resources.source.1.config.requireFileExists': 'false',
        'project.ssh-keypath': '/var/rundeck/.ssh/id_rsa',
        'resources.source.1.type': 'file',
    })
    return config


def update_project_config(name, project, config):
    session, make_url = get_session()
    resp = session.put(
        make_url("/api/18/project/{}/config".format(name)),
        json=config,
        allow_redirects=False,
    )
    if resp.status_code == 201:
        return resp.json()
    LOG.debug("update_project: %s", name)


def delete_project(name):
    session, make_url = get_session()
    resp = session.delete(make_url("/api/18/project/{}".format(name)))
    status_code = resp.status_code
    if status_code != 204:
        raise salt.exceptions.SaltInvocationError(
            "Could not remove project {} from Rundeck {}: {}"
            .format(name, make_url.base_url, status_code))


def get_session():
    def make_url(url):
        return urljoin(make_url.base_url, url)

    rundeck_url = __salt__['config.get']('rundeck.url')
    make_url.base_url = rundeck_url

    api_token = __salt__['config.get']('rundeck.api_token')
    username = __salt__['config.get']('rundeck.username')
    password = __salt__['config.get']('rundeck.password')

    session = requests.Session()

    if api_token:
        session.headers.update({
            'Content-Type': 'application/json',
            'X-Rundeck-Auth-Token': api_token,
        })
    else:
        resp = session.post(make_url('/j_security_check'),
            data={
                'j_username': username,
                'j_password': password,
            },
        )
        if (resp.status_code != 200 or
                '/user/error' in resp.url or
                '/user/login' in resp.url):
            raise salt.exceptions.SaltInvocationError(
                "Username/passowrd authorization failed in Rundeck {} for "
                "user {}".format(rundeck_url, username))
    session.params.update({
        'format': 'json',
    })
    return session, make_url
