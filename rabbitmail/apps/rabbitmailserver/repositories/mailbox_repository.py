from apps.rabbitmailserver.exceptions.exception import InvalidMailboxInRequestException
from apps.rabbitmailserver.models import DefaultMailbox, UserDefinedMailbox


class MailboxRepository:
    def get_default_mailboxes(self):
        return DefaultMailbox.objects.all()

    def get_default_mailbox_by_name(self, mailbox_name):
        try:
            default_mailbox = DefaultMailbox.objects.get(mailbox_name=mailbox_name)
            return default_mailbox
        except DefaultMailbox.DoesNotExist:
            raise InvalidMailboxInRequestException("Mailbox with name: {0} doesn't exist".format(mailbox_name))

    def get_default_mailbox_by_id(self, mailbox_id):
        try:
            default_mailbox = DefaultMailbox.objects.get(pk=mailbox_id)
            return default_mailbox
        except DefaultMailbox.DoesNotExist:
            raise InvalidMailboxInRequestException("Mailbox with id: {0} doesn't exist".format(mailbox_id))

    def get_user_defined_mailboxes(self, user_id):
        return UserDefinedMailbox.objects.filter(user_id=user_id)
