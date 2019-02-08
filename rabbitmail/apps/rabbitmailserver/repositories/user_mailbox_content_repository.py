from apps.rabbitmailserver.exceptions.exception import InvalidUserMailboxContentIdException
from apps.rabbitmailserver.models import UserMailboxContent


class UserMailboxContentRepository:
    def get_user_mailbox_content_by_id(self, user_mailbox_content_id):
        try:
            user_mailbox_content = UserMailboxContent.objects.select_related('mail_content').get(pk=user_mailbox_content_id)
            return user_mailbox_content
        except UserMailboxContent.DoesNotExist:
            raise InvalidUserMailboxContentIdException("User's mailbox mail with mail_id: {0} doesn't exist"
                                                       .format(user_mailbox_content_id))

    def get_user_mailbox_content_by_user_id_and_mail_content_id(self, user_id, mail_content_id):
        try:
            user_mailbox_content = UserMailboxContent.objects.select_related('mail_content')\
                .get(user_id=user_id, mail_content_id=mail_content_id)
            return user_mailbox_content
        except UserMailboxContent.DoesNotExist:
            raise InvalidUserMailboxContentIdException("User's mailbox mail with user_id: {0}, mail_id: {1} "
                                                       "doesn't exist".format(user_id, mail_content_id))

    def save_user_mailbox_content(self, user_mailbox_content):
        user_mailbox_content.save()

    def get_user_mailbox_content_by_user_id_and_default_mailbox_id(self, user_id, default_mailbox_id):
        user_mailbox_contents = UserMailboxContent.objects.select_related('mail_content').filter(
            default_mailbox_id=default_mailbox_id, user_id=user_id)
        return user_mailbox_contents

    def get_user_mailbox_content_by_user_id_and_user_defined_mailbox_id(self, user_id, user_defined_mailbox_id):
        user_mailbox_contents = UserMailboxContent.objects.select_related('mail_content').filter(
            user_defined_mailbox_id=user_defined_mailbox_id, user_id=user_id)
        return user_mailbox_contents

