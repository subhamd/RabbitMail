errors = {}


def get(key):
    return errors.get(key, errors.get(DEFAULT_ERROR))


DEFAULT_ERROR = 100
errors[DEFAULT_ERROR] = {
    'code': DEFAULT_ERROR,
    'msg': 'Oops! Something went wrong. Internal error'
}


USER_NOT_FOUND = 101
errors[USER_NOT_FOUND] = {
    'code': USER_NOT_FOUND,
    'msg': 'User not found'
}

USER_WITH_EMAIL_ID_EXIST = 102
errors[USER_WITH_EMAIL_ID_EXIST] = {
    'code': USER_WITH_EMAIL_ID_EXIST,
    'msg': 'User with email id already exists'
}
