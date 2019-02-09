from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.rabbitmailserver.exceptions import RabbitMailException
from apps.rabbitmailserver.exceptions.exception import MissingRequiredParameterInRequestException
from apps.rabbitmailserver.services.user_mailbox_content_service import UserMailboxContentService
from apps.rabbitmailserver.utils.api_response import APIResponse


class ViewAndDeleteEmail(APIView):
    user_mailbox_content_service = UserMailboxContentService()
    api_response = APIResponse()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ViewAndDeleteEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            user_mailbox_content_id = kwargs.get('mail_id')
            if not user_mailbox_content_id:
                raise MissingRequiredParameterInRequestException('Parameter mail_id is mandatory')

            mail_details = self.user_mailbox_content_service.get_mail_details(user_mailbox_content_id)
            return self.api_response.prep_success_response({'mail': mail_details})
        except RabbitMailException as e:
            return self.api_response.rabbitmail_exception_error_response(e)
        except Exception as e:
            return self.api_response.internal_error_response(str(e))

    def delete(self, request, *args, **kwargs):
        try:
            user_mailbox_content_id = kwargs.get('mail_id')
            if not user_mailbox_content_id:
                raise MissingRequiredParameterInRequestException('Parameter mail_id is mandatory')

            self.user_mailbox_content_service.delete_email_to_trash(user_mailbox_content_id)
            return self.api_response.prep_success_response({'action_response': 'success'})
        except RabbitMailException as e:
            return self.api_response.rabbitmail_exception_error_response(e)
        except Exception as e:
            return self.api_response.internal_error_response(str(e))
