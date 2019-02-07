from apps.rabbitmailserver.exceptions.exception import UserNotFoundException, UserWithEmailIdExistException
from apps.rabbitmailserver.models import User
from apps.rabbitmailserver.repositories.user_repo import UserRepository


class UserService:
    user_repo = UserRepository()

    def create_user(self, first_name, last_name, email_id):
        try:
            user = self.user_repo.get_user_by_email_id(email_id)
            if user:
                raise UserWithEmailIdExistException('A user with email id: {0} already exists'.format(email_id))
        except UserNotFoundException:
            pass

        user = User()
        user.first_name = first_name
        user.last_name = last_name if last_name else ''
        user.email_id = email_id

        self.user_repo.save_user(user)
        return user
