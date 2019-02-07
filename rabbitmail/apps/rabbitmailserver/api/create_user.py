from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.rabbitmailserver.services.user_service import UserService


class CreateUser(APIView):
    user_service = UserService()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CreateUser, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Exception('Method not supported')

    def post(self, request, *args, **kwargs):
        request_data = request.data

        try:
            first_name = request_data.get('first_name')
            last_name = request_data.get('last_name')
            email_id = request_data.get('email_id')

            if not (first_name and email_id):
                raise Exception('Parameter first_name and email_id is mandatory')

            user = self.user_service.create_user(first_name, last_name, email_id)
            return JsonResponse({'user_id': user.id}, status=HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=HTTP_400_BAD_REQUEST)
