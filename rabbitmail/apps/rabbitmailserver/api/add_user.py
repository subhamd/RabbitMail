from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.rabbitmailserver.exceptions import RabbitMailException
from apps.rabbitmailserver.exceptions.exception import MissingRequiredParameterInRequestException
from apps.rabbitmailserver.services.user_service import UserService
from apps.rabbitmailserver.utils.api_response import APIResponse


class AddUser(APIView):
    user_service = UserService()
    api_response = APIResponse()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AddUser, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Exception('Method not supported')

    def post(self, request, *args, **kwargs):
        request_data = request.data

        try:
            first_name = request_data.get('first_name')
            last_name = request_data.get('last_name')
            email_id = request_data.get('email_id')

            if not (first_name and email_id):
                raise MissingRequiredParameterInRequestException('Parameter first_name and email_id is mandatory')

            user = self.user_service.add_user(first_name, last_name, email_id)
            return self.api_response.prep_success_response({'user_id': user.id})
        except RabbitMailException as e:
            return self.api_response.rabbitmail_exception_error_response(e)
        except Exception as e:
            return self.api_response.internal_error_response(str(e))
