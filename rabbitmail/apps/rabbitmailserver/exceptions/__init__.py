from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR


class RabbitMailException(Exception):

    def __init__(self, *args):
        self.message = 'Unhandled exception.'
        self.developer_message = ''
        self.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        self.app_type = 'RABBIT_MAIL_'
        self.error_code = self.app_type + "1000"
        super(RabbitMailException, self).__init__(*args)
