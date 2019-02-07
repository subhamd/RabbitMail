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
