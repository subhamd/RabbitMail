from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.rabbitmailserver.services.mailbox_service import MailboxService


class GetMailboxes(APIView):
    mailbox_service = MailboxService()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(GetMailboxes, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            if not user_id:
                raise Exception('Parameter user_id is mandatory')

            mailboxes = self.mailbox_service.get_all_mailboxes(user_id)
            return JsonResponse(mailboxes, status=HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=HTTP_400_BAD_REQUEST)
