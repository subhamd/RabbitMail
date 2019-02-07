from apps.rabbitmailserver.exceptions.exception import UserNotFoundException
from apps.rabbitmailserver.models import User


class UserRepository:
    def get_user_by_id(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise UserNotFoundException("User with id: {0} doesn't exist".format(user_id))

    def get_user_by_email_id(self, email_id):
        try:
            user = User.objects.get(email_id=email_id)
            return user
        except User.DoesNotExist:
            raise UserNotFoundException("User with email_id: {0} doesn't exist".format(email_id))

    def save_user(self, user):
        user.save()


