import logging

LOG = logging.getLogger(__name__)


def __virtual__():
    if 'rundeck.get_project' not in __salt__:
        return (
            False,
            'The rundeck_project state module cannot be loaded: rundeck is '
            'unavailable',
        )
    return True


def present(name, description=''):
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
    }
    if __opts__['test'] == True:
        ret['comment'] = 'Nothing to change in the test mode.'
        ret['result'] = None
        return ret
    params = {
        "description": description,
    }
    project = __salt__['rundeck.get_project'](name)
    if project:
        config = __salt__['rundeck.create_project_config'](
            name, params, config=project["config"])
        if project["config"] != config:
            LOG.warning("{}: {}".format(project["config"], config))
            __salt__['rundeck.update_project_config'](name, project, config)
            ret['comment'] = "Project {} was updated.".format(name)
            ret['changes'][name] = 'UPDATED'
        else:
            ret['comment'] = "Project {} is already up to date.".format(name)
    else:
        __salt__['rundeck.create_project'](name, params)
        ret['comment'] = "Project {} was created.".format(name)
        ret['changes'][name] = 'CREATED'
    ret['result'] = True
    return ret


def absent(name):
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
    }
    if __opts__['test'] == True:
        ret['comment'] = 'Nothing to remove in the test mode.'
        ret['result'] = None
        return ret
    project = __salt__['rundeck.get_project'](name)
    if project:
        __salt__['rundeck.delete_project'](name)
        ret['changes'][name] = 'DELETED'
        ret['comment'] = "Project {} was removed.".format(name)
    ret['result'] = True
    return ret
