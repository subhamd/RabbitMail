from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from apps.rabbitmailserver.exceptions import RabbitMailException
from apps.rabbitmailserver.exceptions.exception import MissingRequiredParameterInRequestException
from apps.rabbitmailserver.services.user_mailbox_content_service import UserMailboxContentService
from apps.rabbitmailserver.utils.api_response import APIResponse


class SendEmail(APIView):
    user_mailbox_content_service = UserMailboxContentService()
    api_response = APIResponse()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SendEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Exception('Method not supported')

    def post(self, request, *args, **kwargs):
        try:
            user_mailbox_content_id = kwargs.get('mail_id')
            if not user_mailbox_content_id:
                raise MissingRequiredParameterInRequestException("Parameter mail_id is mandatory")

            user_mailbox_content = \
                self.user_mailbox_content_service.get_user_mailbox_content_by_id(user_mailbox_content_id)

            internal_recipients, external_recipients = \
                self.user_mailbox_content_service.send_mail(user_mailbox_content)

            mail_sending_response = []
            for internal_recipient in internal_recipients:
                mail_sending_response.append({
                    'email_id': internal_recipient,
                    'status': 'Email sent',
                    'user_type': 'System user'
                })
            for external_recipient in external_recipients:
                mail_sending_response.append({
                    'email_id': external_recipient,
                    'status': 'Email sent',
                    'user_type': 'External user'
                })
            data = {'action_response': mail_sending_response}

            return self.api_response.prep_success_response({'data': data})
        except RabbitMailException as e:
            return self.api_response.rabbitmail_exception_error_response(e)
        except Exception as e:
            return self.api_response.internal_error_response(str(e))

