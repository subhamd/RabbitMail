from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


class ForwardEmail(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ForwardEmail, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Exception('Method not supported')

    def post(self, request, *args, **kwargs):
        pass

