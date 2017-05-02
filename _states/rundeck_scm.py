import logging

LOG = logging.getLogger(__name__)


def __virtual__():
    if 'rundeck.get_project' not in __salt__:
        return (
            False,
            'The rundeck_scm state module cannot be loaded: rundeck is '
            'unavailable',
        )
    return True


def present_import(name, project_name, **params):
    result = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
    }
    if __opts__['test'] == True:
        result['comment'] = 'There is nothing to change in the test mode.'
        result['result'] = None
    ok, plugin = __salt__['rundeck.get_plugin'](project_name, 'import')
    if ok:
        if plugin:
            config = __salt__['rundeck.create_scm_import_config'](
                project_name, params, config=plugin['config'])
            LOG.debug("SCM Import for the %s project: %s/%s",
                      project_name, plugin["config"], config)
            if plugin['config'] != config:
                ok, plugin = __salt__['rundeck.update_scm_import_config'](
                    project_name, plugin, config)
                result['comment'] = (
                    "SCM Import plugin for the {} project was updated."
                    .format(project_name))
                result['changes'][name] = 'UPDATED'
            else:
                result['comment'] = (
                    "SCM Import plugin for the {} project is already up to "
                    "date.".format(project_name))
            result['result'] = True
        else:
            ok, plugin = __salt__['rundeck.setup_scm_import'](
                project_name, params)
            if ok:
                result['changes'][name] = 'CREATED'
                result['comment'] = (
                    "SCM Import was configured for the {} project."
                    .format(project_name))
                result['result'] = True
            else:
                result['comment'] = plugin
    else:
        result['comment'] = plugin
    return result


def sync_import(name, project_name, **params):
    result = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': '',
        'pchanges': {},
    }

    if __opts__['test'] == True:
        result['comment'] = 'There is nothing to change in the test mode.'
        result['result'] = None
        return result

    ok, plugin = __salt__['rundeck.get_plugin'](project_name, 'import')
    if not ok:
        result['comment'] = plugin
        return result

    ok, state = __salt__['rundeck.get_plugin_state'](project_name, 'import')
    if not ok:
        result['comment'] = state
        return result

    history = []

    for action_name, action in [
            ('initialize-tracking', 'rundeck.perform_scm_import_tracking'),
            ('remote-pull', 'rundeck.perform_scm_import_pull'),
            ('import-all', 'rundeck.perform_scm_import'),
            ]:
        if action_name in state['actions']:
            ok, msg = __salt__[action](
                project_name, plugin, params)
            if not ok:
                result['comment'] = msg
                result['result'] = False
                return result
            else:
                history.append(msg['message'])

            ok, state = __salt__['rundeck.get_plugin_state'](
                project_name, 'import')
            if not ok:
                result['comment'] = state
                result['result'] = False
                return result

    if history:
        result['changes'][name] = '\n'.join(history)
    return result


def disabled_import(name, project_name):
    result = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
    }
    if __opts__['test'] == True:
        result['comment'] = 'There is nothing to change in the test mode.'
        result['result'] = None
    ok, status = __salt__['rundeck.get_plugin_status'](project_name, 'import')
    if ok:
        if status['enabled']:
            ok, msg = __salt__['rundeck.disable_plugin'](project_name, 'import')
            result['comment'] = msg
            if ok:
                result['changes'][name] = 'DISABLED'
                result['result'] = True
        else:
            result['result'] = True
    else:
        result['comment'] = status
    return result


def enabled_import(name, project_name):
    result = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
    }
    if __opts__['test'] == True:
        result['comment'] = 'There is nothing to change in the test mode.'
        result['result'] = None
    ok, status = __salt__['rundeck.get_plugin_status'](project_name, 'import')
    if ok:
        if status['configured'] and not status['enabled']:
            ok, msg = __salt__['rundeck.enable_plugin'](project_name, 'import')
            result['comment'] = msg
            if ok:
                result['changes'][name] = 'ENABLED'
                result['result'] = True
        elif not status['configured']:
            result['comment'] = "Could not enable not configured SCM plugin."
        else:
            result['result'] = True
    else:
        result['comment'] = status
    return result
