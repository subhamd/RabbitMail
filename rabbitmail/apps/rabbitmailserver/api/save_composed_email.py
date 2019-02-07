from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.rabbitmailserver.services.mail_content_service import MailContentService
from apps.rabbitmailserver.services.user_mailbox_content_service import UserMailboxContentService


class SaveComposedEmail(APIView):
    mail_content_service = MailContentService()
    user_mailbox_content_service = UserMailboxContentService()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SaveComposedEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Exception('Method not supported')

    def post(self, request, *args, **kwargs):
        request_data = request.data

        try:
            recipients = request_data.get('to')
            sender_user_id = request_data.get('user_id')
            subject = request_data.get('subject')
            body = request_data.get('body')
            associated_mail_id = request_data.get('associated_mail_id')

            if not sender_user_id:
                raise Exception("Parameter user_id is mandatory")

            if not(recipients or subject or body or associated_mail_id):
                raise Exception("At least one parameter is required: to, subject, body, associated_mail_id")

            mail_content = self.mail_content_service.add_mail_content(sender_user_id,
                                                                      recipients,
                                                                      subject,
                                                                      body,
                                                                      associated_mail_id)
            self.user_mailbox_content_service.add_user_mailbox_content(sender_user_id, mail_content)
            return JsonResponse({'mail_id': mail_content.id}, status=HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=HTTP_400_BAD_REQUEST)
