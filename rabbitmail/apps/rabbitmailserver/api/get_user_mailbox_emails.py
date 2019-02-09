from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.rabbitmailserver.exceptions import RabbitMailException
from apps.rabbitmailserver.exceptions.exception import MissingRequiredParameterInRequestException, \
    InvalidMailboxTypeInRequestException
from apps.rabbitmailserver.services.user_mailbox_content_service import UserMailboxContentService
from apps.rabbitmailserver.utils.api_response import APIResponse


class GetUserMailboxEmails(APIView):
    user_mailbox_content_service = UserMailboxContentService()
    api_response = APIResponse()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(GetUserMailboxEmails, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        request_data = request.data

        try:
            user_id = kwargs.get('user_id')
            mailbox_id = kwargs.get('mailbox_id')
            if not (user_id and mailbox_id):
                raise MissingRequiredParameterInRequestException('Parameter user_id and mailbox_id is mandatory')

            mailbox_type = request_data.get('mailbox_type', 'default')
            if mailbox_type not in ['default', 'user_defined']:
                raise InvalidMailboxTypeInRequestException('Invalid mailbox type: {0} in request. Supported values: '
                                                           'default, user_defined'.format(mailbox_type))

            if mailbox_type == 'default':
                mails = self.user_mailbox_content_service.get_default_mailbox_mails(user_id, mailbox_id)
            else:
                mails = self.user_mailbox_content_service.get_user_defined_mailbox_mails(user_id, mailbox_id)

            return self.api_response.prep_success_response({'mails': mails})
        except RabbitMailException as e:
            return self.api_response.rabbitmail_exception_error_response(e)
        except Exception as e:
            return self.api_response.internal_error_response(str(e))

