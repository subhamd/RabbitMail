from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from apps.rabbitmailserver.exceptions.exception import MissingRequiredParameterInRequestException
from apps.rabbitmailserver.services.mail_content_service import MailContentService
from apps.rabbitmailserver.services.user_mailbox_content_service import UserMailboxContentService


class ReplyToEmail(APIView):
    mail_content_service = MailContentService()
    user_mailbox_content_service = UserMailboxContentService()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReplyToEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Exception('Method not supported')

    def post(self, request, *args, **kwargs):
        request_data = request.data

        try:
            subject = request_data.get('subject')
            body = request_data.get('body')
            user_mailbox_content_id = kwargs.get('mail_id')

            if not (user_mailbox_content_id and body):
                raise MissingRequiredParameterInRequestException("Parameter mail_id and body are mandatory")

            user_mailbox_content = \
                self.user_mailbox_content_service.get_user_mailbox_content_by_id(user_mailbox_content_id)

            if not subject:
                subject = 'Re: ' + user_mailbox_content.mail_content.subject

            new_mail_content = self.mail_content_service.add_mail_content(
                sender=user_mailbox_content.user,
                recipients=user_mailbox_content.mail_content.sender_email_id,
                subject=subject,
                body=body,
                associated_mail_id=user_mailbox_content.mail_content.id
            )

            new_user_mailbox_content = \
                self.user_mailbox_content_service.add_user_mailbox_content(user_mailbox_content.user, new_mail_content)

            internal_recipients, external_recipients = \
                self.user_mailbox_content_service.send_mail(new_user_mailbox_content)

            data = {
                'mail_id': new_user_mailbox_content.id,
            }

            mail_replying_response = []
            for internal_recipient in internal_recipients:
                mail_replying_response.append({
                    'email_id': internal_recipient,
                    'status': 'Email sent',
                    'user_type': 'System user'
                })
            for external_recipient in external_recipients:
                mail_replying_response.append({
                    'email_id': external_recipient,
                    'status': 'Email sent',
                    'user_type': 'External user'
                })
            data['action_response'] = mail_replying_response

            return JsonResponse({'data': data}, status=HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=HTTP_400_BAD_REQUEST)

