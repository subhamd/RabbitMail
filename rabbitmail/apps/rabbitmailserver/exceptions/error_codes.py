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

MISSING_REQUIRED_PARAMETER_IN_REQUEST = 103
errors[MISSING_REQUIRED_PARAMETER_IN_REQUEST] = {
    'code': MISSING_REQUIRED_PARAMETER_IN_REQUEST,
    'msg': 'Missing required parameter in request'
}

INVALID_MAIL_CONTENT_ID = 104
errors[INVALID_MAIL_CONTENT_ID] = {
    'code': INVALID_MAIL_CONTENT_ID,
    'msg': 'Invalid argument mail_id'
}

INVALID_USER_MAILBOX_CONTENT_ID = 105
errors[INVALID_USER_MAILBOX_CONTENT_ID] = {
    'code': INVALID_USER_MAILBOX_CONTENT_ID,
    'msg': 'Invalid argument user_mailbox_content_id'
}

INVALID_MAILBOX_TYPE_IN_REQUEST = 106
errors[INVALID_MAILBOX_TYPE_IN_REQUEST] = {
    'code': INVALID_MAILBOX_TYPE_IN_REQUEST,
    'msg': 'Invalid mailbox type in request'
}

INVALID_MAILBOX_IN_REQUEST = 107
errors[INVALID_MAILBOX_IN_REQUEST] = {
    'code': INVALID_MAILBOX_IN_REQUEST,
    'msg': 'Invalid mailbox in request'
}

MAIL_ALREADY_SENT = 108
errors[MAIL_ALREADY_SENT] = {
    'code': MAIL_ALREADY_SENT,
    'msg': 'Mail already sent'
}
