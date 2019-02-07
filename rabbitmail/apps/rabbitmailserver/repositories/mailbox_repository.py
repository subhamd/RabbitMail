from apps.rabbitmailserver.models import DefaultMailbox, UserDefinedMailbox


class MailboxRepository:
    def get_default_mailboxes(self):
        return DefaultMailbox.objects.all()

    def get_default_mailbox_by_name(self, mailbox_name):
        return DefaultMailbox.objects.get(mailbox_name=mailbox_name)

    def get_user_mailboxes(self, user_id):
        return UserDefinedMailbox.objects.filter(user_id=user_id)
