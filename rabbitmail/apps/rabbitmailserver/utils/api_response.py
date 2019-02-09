from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from rest_framework.utils.serializer_helpers import ReturnDict


class APIResponse(object):
    @classmethod
    def rabbitmail_exception_error_response(cls, e):
        developer_message = None
        if hasattr(e, 'developer_message'):
            developer_message = e.developer_message

        return cls.__prep_error_response(error_code=e.error_code,
                                         message=e.message,
                                         response_code=e.status_code,
                                         developer_message=developer_message,
                                         error_type="logical_error")

    @classmethod
    def internal_error_response(cls, message):
        error_code = 'RABBIT_MAIL__1000'
        return cls.__prep_error_response(error_code=error_code,
                                         message=message,
                                         response_code=HTTP_500_INTERNAL_SERVER_ERROR,
                                         error_type="unknown_error")

    @classmethod
    def __prep_error_response(cls, error_code, message, response_code,
                              developer_message=None, error_type="unknown_error"):
        """
        prepares a Response object in the standard format
        :param errors: error codes and messages explaining/accompanying the error
        :return: Response object
        """
        error = {
                "code": error_code,
                "message": message,
                "error_type": error_type,
            }

        if developer_message:
            error['developer_message'] = developer_message

        error_response = {
            "errors": [error]
        }

        response = Response(data=error_response, status=response_code)
        return response

    @classmethod
    def prep_success_response(cls, message, response_code=HTTP_200_OK):
        """
        vanilla Response object on success
        :param message: what message to embed as part of the response
        :param response_code: what http response code to use
        :return: Response object
        """
        if type(message) in (dict, ReturnDict):
            response = message
        else:
            response = {
                "message": message
            }
        response = Response(data=response, status=response_code)
        return response
