from rest_framework.status import HTTP_400_BAD_REQUEST

from apps.rabbitmailserver.exceptions import RabbitMailException, error_codes
from apps.rabbitmailserver.exceptions.error_codes import errors


class UserNotFoundException(RabbitMailException):
    def __init__(self, developer_message, *args, **kwargs):
        super(UserNotFoundException, self).__init__()
        error = errors.get(error_codes.USER_NOT_FOUND)
        self.message = error['msg']
        self.developer_message = developer_message
        self.status_code = HTTP_400_BAD_REQUEST
        self.error_code = self.app_type + str(error['code'])


class UserWithEmailIdExistException(RabbitMailException):
    def __init__(self, developer_message, *args, **kwargs):
        super(UserWithEmailIdExistException, self).__init__()
        error = errors.get(error_codes.USER_WITH_EMAIL_ID_EXIST)
        self.message = error['msg']
        self.developer_message = developer_message
        self.status_code = HTTP_400_BAD_REQUEST
        self.error_code = self.app_type + str(error['code'])


class MissingRequiredParameterInRequestException(RabbitMailException):
    def __init__(self, developer_message, *args, **kwargs):
        super(MissingRequiredParameterInRequestException, self).__init__()
        error = errors.get(error_codes.MISSING_REQUIRED_PARAMETER_IN_REQUEST)
        self.message = error['msg']
        self.developer_message = developer_message
        self.status_code = HTTP_400_BAD_REQUEST
        self.error_code = self.app_type + str(error['code'])


class InvalidMailContentIdException(RabbitMailException):
    def __init__(self, developer_message, *args, **kwargs):
        super(InvalidMailContentIdException, self).__init__()
        error = errors.get(error_codes.INVALID_MAIL_CONTENT_ID)
        self.message = error['msg']
        self.developer_message = developer_message
        self.status_code = HTTP_400_BAD_REQUEST
        self.error_code = self.app_type + str(error['code'])


class InvalidUserMailboxContentIdException(RabbitMailException):
    def __init__(self, developer_message, *args, **kwargs):
        super(InvalidUserMailboxContentIdException, self).__init__()
        error = errors.get(error_codes.INVALID_USER_MAILBOX_CONTENT_ID)
        self.message = error['msg']
        self.developer_message = developer_message
        self.status_code = HTTP_400_BAD_REQUEST
        self.error_code = self.app_type + str(error['code'])


class InvalidMailboxTypeInRequestException(RabbitMailException):
    def __init__(self, developer_message, *args, **kwargs):
        super(InvalidMailboxTypeInRequestException, self).__init__()
        error = errors.get(error_codes.INVALID_MAILBOX_TYPE_IN_REQUEST)
        self.message = error['msg']
        self.developer_message = developer_message
        self.status_code = HTTP_400_BAD_REQUEST
        self.error_code = self.app_type + str(error['code'])


class InvalidMailboxInRequestException(RabbitMailException):
    def __init__(self, developer_message, *args, **kwargs):
        super(InvalidMailboxInRequestException, self).__init__()
        error = errors.get(error_codes.INVALID_MAILBOX_IN_REQUEST)
        self.message = error['msg']
        self.developer_message = developer_message
        self.status_code = HTTP_400_BAD_REQUEST
        self.error_code = self.app_type + str(error['code'])


class MailAlreadySentException(RabbitMailException):
    def __init__(self, *args, **kwargs):
        super(MailAlreadySentException, self).__init__()
        error = errors.get(error_codes.MAIL_ALREADY_SENT)
        self.message = error['msg']
        self.status_code = HTTP_400_BAD_REQUEST
        self.error_code = self.app_type + str(error['code'])
