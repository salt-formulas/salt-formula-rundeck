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


def present(name, type, content):
    result = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
    }
    if __opts__['test'] == True:
        result['comment'] = 'Nothing to create in the test mode.'
        result['result'] = None
        return result
    ok, secret = __salt__['rundeck.get_secret_metadata'](name)
    if ok:
        do_update = secret is not None
        ok, msg = __salt__['rundeck.upload_secret'](name, type, content,
                                                    update=do_update)
        if ok:
            result['changes'][name] = 'UPLOADED'
            result['comment'] = (
                "The {} secret key with the {} type was successfully uploaded."
                .format(name, type))
            result['result'] = True
        else:
            result['comment'] = msg
    else:
        result['comment'] = secret
    return result


def absent(name):
    result = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
    }
    if __opts__['test'] == True:
        result['comment'] = 'Nothing to remove in the test mode.'
        result['result'] = None
        return result
    ok, secret = __salt__['rundeck.get_secret_metadata'](name)
    if ok:
        if not secret:
            result['result'] = True
            return result
        ok, msg = __salt__['rundeck.delete_secret'](name)
        if ok:
            result['changes'][name] = 'DELETED'
            result['comment'] = "Secret key {} was removed.".format(name)
            result['result'] = True
        else:
            result['comment'] = msg
    else:
        result['comment'] = secret
    return result
