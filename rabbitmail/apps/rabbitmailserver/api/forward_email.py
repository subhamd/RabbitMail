from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from apps.rabbitmailserver.exceptions import RabbitMailException
from apps.rabbitmailserver.exceptions.exception import MissingRequiredParameterInRequestException
from apps.rabbitmailserver.services.mail_content_service import MailContentService
from apps.rabbitmailserver.services.user_mailbox_content_service import UserMailboxContentService
from apps.rabbitmailserver.utils.api_response import APIResponse


class ForwardEmail(APIView):
    mail_content_service = MailContentService()
    user_mailbox_content_service = UserMailboxContentService()
    api_response = APIResponse()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ForwardEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Exception('Method not supported')

    def post(self, request, *args, **kwargs):
        request_data = request.data

        try:
            recipients = request_data.get('to')
            subject = request_data.get('subject')
            user_mailbox_content_id = kwargs.get('mail_id')

            if not (recipients and user_mailbox_content_id):
                raise MissingRequiredParameterInRequestException("Parameter to and mail_id are mandatory")

            user_mailbox_content = \
                self.user_mailbox_content_service.get_user_mailbox_content_by_id(user_mailbox_content_id)

            if not subject:
                subject = 'Fwd: ' + user_mailbox_content.mail_content.subject

            new_mail_content = self.mail_content_service.add_mail_content(
                sender=user_mailbox_content.user,
                recipients=recipients,
                subject=subject,
                body=user_mailbox_content.mail_content.body,
                associated_mail_id=user_mailbox_content.mail_content.id
            )

            new_user_mailbox_content = \
                self.user_mailbox_content_service.add_user_mailbox_content(user_mailbox_content.user, new_mail_content)

            internal_recipients, external_recipients = \
                self.user_mailbox_content_service.send_mail(new_user_mailbox_content)

            data = {
                'mail_id': new_user_mailbox_content.id,
            }

            mail_forwarding_response = []
            for internal_recipient in internal_recipients:
                mail_forwarding_response.append({
                    'email_id': internal_recipient,
                    'status': 'Email forwarded',
                    'user_type': 'System user'
                })
            for external_recipient in external_recipients:
                mail_forwarding_response.append({
                    'email_id': external_recipient,
                    'status': 'Email forwarded',
                    'user_type': 'External user'
                })
            data['action_response'] = mail_forwarding_response

            return self.api_response.prep_success_response({'data': data})
        except RabbitMailException as e:
            return self.api_response.rabbitmail_exception_error_response(e)
        except Exception as e:
            return self.api_response.internal_error_response(str(e))

