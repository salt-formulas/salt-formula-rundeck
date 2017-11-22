import logging

import salt.exceptions

import requests
from requests.compat import urljoin

LOG = logging.getLogger(__name__)


# Project

def get_project(name):
    session, make_url = get_session()
    resp = session.get(make_url("/api/18/project/{}".format(name)))
    status_code = resp.status_code
    if status_code == 200:
        return resp.json()
    elif status_code == 404:
        return None
    raise salt.exceptions.SaltInvocationError(
        "Could not retrieve information about project {} from Rundeck {}: "
        "{}/{}".format(name, make_url.base_url, status_code, resp.text))


def create_project(name, params):
    session, make_url = get_session()
    config = create_project_config(name, params)
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


def update_project_config(name, project, config):
    session, make_url = get_session()
    resp = session.put(
        make_url("/api/18/project/{}/config".format(name)),
        json=config,
        allow_redirects=False,
    )
    if resp.status_code == 201:
        return resp.json()


def delete_project(name):
    session, make_url = get_session()
    resp = session.delete(make_url("/api/18/project/{}".format(name)))
    status_code = resp.status_code
    if status_code != 204:
        raise salt.exceptions.SaltInvocationError(
            "Could not remove project {} from Rundeck {}: {}/{}"
            .format(name, make_url.base_url, status_code, resp.text))


# SCM

def get_plugin(project_name, integration):
    session, make_url = get_session()
    resp = session.get(make_url("/api/18/project/{}/scm/{}/config"
                                .format(project_name, integration)))
    if resp.status_code == 200:
        return True, resp.json()
    elif resp.status_code == 404:
        return True, None
    return False, (
        "Could not get config for the {} plugin of the {} project: {}"
        .format(integration, project_name, resp.text))


def get_plugin_status(project_name, integration):
    def get_plugin(plugins, plugin_type):
        for plugin in plugins:
            if plugin['type'] == plugin_type:
                return plugin
        LOG.debug(
            "Could not find the %s integration among available plugins of "
            "the %s projects: %s", integration, project_name, plugins)
        raise salt.exceptions.SaltInvocationError(
            "Could not find status for the {}/{} plugin of the {} project, "
            "this integration is not available in your deployment."
            .format(integration, plugin_type, project_name))

    session, make_url = get_session()
    resp = session.get(make_url("/api/18/project/{}/scm/{}/plugins"
                                .format(project_name, integration)))
    if resp.status_code == 200:
        plugin_type = "git-{}".format(integration)
        status = get_plugin(resp.json()['plugins'], plugin_type)
        return True, status
    return False, (
        "Could not get status for the {} plugin of the {} project: {}"
        .format(integration, project_name, resp.text))


def get_plugin_state(project_name, integration):
    session, make_url = get_session()
    resp = session.get(make_url("/api/18/project/{}/scm/{}/status"
                                .format(project_name, integration)))
    if resp.status_code == 200:
        return True, resp.json()
    return False, (
        "Could not get state for the {} plugin of the {} project: {}"
        .format(integration, project_name, resp.text))


def disable_plugin(project_name, integration):
    session, make_url = get_session()
    resp = session.post(make_url(
        "/api/15/project/{}/scm/{}/plugin/git-{}/disable"
        .format(project_name, integration, integration)))
    if resp.status_code == 200:
        msg = resp.json()
        return True, msg['message']
    return False, (
        "Could not disable the {} plugin for the {} project: {}/{}"
        .format(integration, project_name, resp.status_code, resp.text))


def enable_plugin(project_name, integration):
    session, make_url = get_session()
    resp = session.post(make_url(
        "/api/15/project/{}/scm/{}/plugin/git-{}/enable"
        .format(project_name, integration, integration)))
    if resp.status_code == 200:
        msg = resp.json()
        return True, msg['message']
    return False, (
        "Could not enable the {} plugin for the {} project: {}/{}"
        .format(integration, project_name, resp.status_code, resp.text))


# SCM Import

def setup_scm_import(project_name, params):
    session, make_url = get_session()
    config = create_scm_import_config(project_name, params)
    resp = session.post(
        make_url("/api/15/project/{}/scm/import/plugin/git-import/setup"
                 .format(project_name)),
        json={
            'config': config,
        },
        allow_redirects=False,
    )
    if resp.status_code == 200:
        return True, resp.json()
    return False, (
        "Could not configure SCM Import for the {} project: {}/{}"
        .format(project_name, resp.status_code, resp.text))


def update_scm_import_config(project_name, plugin, config):
    session, make_url = get_session()
    resp = session.post(
        make_url("/api/15/project/{}/scm/import/plugin/git-import/setup"
                 .format(project_name)),
        json={
            'config': config,
        },
        allow_redirects=False,
    )
    if resp.status_code == 200:
        return True, resp.json()
    return False, (
        "Could not update SCM Import for the {} project: {}/{}"
        .format(project_name, resp.status_code, resp.text))


def perform_scm_import_tracking(project_name, plugin, params):
    format = plugin['config']['format']
    file_pattern = params.get('file_pattern')
    if not file_pattern:
        file_pattern = DEFAULT_FILE_PATTERNS[format]

    session, make_url = get_session()
    resp = session.post(
        make_url("/api/15/project/{}/scm/import/action/initialize-tracking"
                 .format(project_name)),
        json={
            'input': {
                'filePattern': file_pattern,
                'useFilePattern': 'true',
            },
            'jobs': [],
            'items': [],
            'deleted': [],
        },
        allow_redirects=False,
    )
    if resp.status_code == 200:
        return True, resp.json()
    return False, (
        "Could not update SCM Import for the {} project: {}/{}"
        .format(project_name, resp.status_code, resp.text))

DEFAULT_FILE_PATTERNS = {
    'yaml': r'.*\.yaml',
    'xml': r'.*\.xml',
}


def perform_scm_import_pull(project_name, plugin, params):
    session, make_url = get_session()
    resp = session.post(
        make_url("/api/15/project/{}/scm/import/action/remote-pull"
                 .format(project_name)),
        json={
            'input': {},
            'jobs': [],
            'items': [],
            'deleted': [],
        },
        allow_redirects=False,
    )
    if resp.status_code == 200:
        return True, resp.json()
    return False, (
        "Could not pull remote changes for the {} project: {}/{}"
        .format(project_name, resp.status_code, resp.text))


def perform_scm_import(project_name, plugin, params):
    session, make_url = get_session()
    ok, inputs = get_plugin_action_inputs(
        project_name, 'import', 'import-all')
    if not ok:
        return False, inputs
    items = list(item['itemId'] for item in inputs['importItems'])
    resp = session.post(
        make_url("/api/15/project/{}/scm/import/action/import-all"
                 .format(project_name)),
        json={
            'input': {},
            'jobs': [],
            'items': items,
            'deleted': [],
        },
        allow_redirects=False,
    )
    if resp.status_code == 200:
        return True, resp.json()
    return False, (
        "Could not import jobs for the {} project: {}/{}"
        .format(project_name, resp.status_code, resp.text))


# Key Store

def get_secret_metadata(path):
    session, make_url = get_session()
    resp = session.get(
        make_url("/api/11/storage/keys/{}".format(path)),
        allow_redirects=False,
    )
    if resp.status_code == 200:
        return True, resp.json()
    elif resp.status_code == 404:
        return True, None
    return False, (
        "Could not retrieve metadata for the {} secret key: {}/{}"
        .format(path, resp.status_code, resp.text))


def upload_secret(path, type, content, update=False):
    session, make_url = get_session()
    session.headers['Content-Type'] = SECRET_CONTENT_TYPE[type]
    method = session.put if update else session.post
    resp = method(
        make_url("/api/11/storage/keys/{}".format(path)),
        data=content,
        allow_redirects=False,
    )
    if resp.status_code in (200, 201):
        return True, resp.json()
    return False, (
        "Could not create or update the {} secret key with the type {}: {}/{}"
        .format(path, type, resp.status_code, resp.text))

SECRET_CONTENT_TYPE = {
    "private": "application/octet-stream",
    "public": "application/pgp-keys",
    "password": "application/x-rundeck-data-password",
}


def delete_secret(path):
    session, make_url = get_session()
    resp = session.delete(
        make_url("/api/11/storage/keys/{}".format(path)),
        allow_redirects=False,
    )
    if resp.status_code == 204:
        return True, None
    return False, (
        "Could not delete the {} secret key: {}/{}"
        .format(path, resp.status_code, resp.text))


# Utils

def create_project_config(project_name, params, config=None):
    config = dict(config) if config else {}
    if params['description']:
       config['project.description'] = params['description']
    else:
       config.pop('project.description', None)
    config.update({
        'resources.source.1.config.file':
            "/var/rundeck/projects/{}/etc/resources.yaml".format(project_name),
        'resources.source.1.config.format': 'resourceyaml',
        'resources.source.1.config.generateFileAutomatically': 'true',
        'resources.source.1.config.includeServerNode': 'false',
        'resources.source.1.config.requireFileExists': 'false',
        'project.ssh-keypath': '/var/rundeck/.ssh/id_rsa',
        'resources.source.1.type': 'file',
    })
    return config


def create_scm_import_config(project_name, params, config=None):
    config = dict(config) if config else {}

    format = params.get('format', 'yaml')
    if format not in DEFAULT_FILE_PATTERNS:
        supported_formats = DEFAULT_FILE_PATTERNS.keys()
        raise salt.exceptions.SaltInvocationError(
            "Unsupported format {} for the {} SCM import module, should be {}"
            .format(format, project_name, ','.join(supported_formats)))

    config.update({
        'dir': "/var/rundeck/projects/{}/scm".format(project_name),
        'url': params['address'],
        'branch': params.get('branch', 'master'),
        'fetchAutomatically': 'true',
        'format': format,
        'pathTemplate': params.get(
            'path_template', '${job.group}${job.name}.${config.format}'),
        'importUuidBehavior': params.get('import_uuid_behavior', 'remove'),
        'strictHostKeyChecking': 'yes',
    })
    return config


def get_plugin_action_inputs(project_name, integration, action):
    session, make_url = get_session()
    resp = session.get(
        make_url("/api/18/project/cicd/scm/import/action/import-all/input"))
    if resp.status_code == 200:
        return True, resp.json()
    return False, (
        "Could not get inputs for the {} action for the {} project: {}/{}"
        .format(action, project_name, resp.status_code, resp.text))



def get_session():
    def make_url(url):
        return urljoin(make_url.base_url, url)

    rundeck_url = __salt__['config.get']('rundeck.url')
    api_token = __salt__['config.get']('rundeck.api_token')
    username = __salt__['config.get']('rundeck.username')
    password = __salt__['config.get']('rundeck.password')

    if not rundeck_url:
        raise salt.exceptions.SaltInvocationError(
            "The 'rundeck.url' parameter have to be set as non-empty value in "
            "the minion's configuration file.")
    elif not (api_token or username and password):
        raise salt.exceptions.SaltInvocationError(
            "Either the 'rundeck.api_token' parameter or a pair of "
            "'rundeck.username' and 'rundeck.password' parameters have to be "
            "set as non-empty values in the minion's configuration file.")

    make_url.base_url = rundeck_url

    session = requests.Session()

    if api_token:
        session.headers.update({
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
                "Username/password authorization failed in Rundeck {} for "
                "user {}".format(rundeck_url, username))
    session.params.update({
        'format': 'json',
    })
    return session, make_url
