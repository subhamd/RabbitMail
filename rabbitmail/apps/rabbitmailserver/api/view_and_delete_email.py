from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.rabbitmailserver.exceptions.exception import MissingRequiredParameterInRequestException
from apps.rabbitmailserver.services.user_mailbox_content_service import UserMailboxContentService


class ViewAndDeleteEmail(APIView):
    user_mailbox_content_service = UserMailboxContentService()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ViewAndDeleteEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            user_mailbox_content_id = kwargs.get('mail_id')
            if not user_mailbox_content_id:
                raise MissingRequiredParameterInRequestException('Parameter mail_id is mandatory')

            mail_details = self.user_mailbox_content_service.get_mail_details(user_mailbox_content_id)
            return JsonResponse({'mail': mail_details}, status=HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            user_mailbox_content_id = kwargs.get('mail_id')
            if not user_mailbox_content_id:
                raise MissingRequiredParameterInRequestException('Parameter mail_id is mandatory')

            self.user_mailbox_content_service.delete_email_to_trash(user_mailbox_content_id)
            return JsonResponse({'action_response': 'success'}, status=HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=HTTP_400_BAD_REQUEST)
