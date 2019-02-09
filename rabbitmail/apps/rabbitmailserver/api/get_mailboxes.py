from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.rabbitmailserver.exceptions import RabbitMailException
from apps.rabbitmailserver.exceptions.exception import MissingRequiredParameterInRequestException
from apps.rabbitmailserver.services.mailbox_service import MailboxService
from apps.rabbitmailserver.utils.api_response import APIResponse


class GetMailboxes(APIView):
    mailbox_service = MailboxService()
    api_response = APIResponse()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(GetMailboxes, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            if not user_id:
                raise MissingRequiredParameterInRequestException('Parameter user_id is mandatory')

            mailboxes = self.mailbox_service.get_all_mailboxes(user_id)
            return self.api_response.prep_success_response(mailboxes)
        except RabbitMailException as e:
            return self.api_response.rabbitmail_exception_error_response(e)
        except Exception as e:
            return self.api_response.internal_error_response(str(e))
