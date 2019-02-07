from apps.rabbitmailserver.repositories.mailbox_repository import MailboxRepository


class MailboxService:
    mailbox_repo = MailboxRepository()

    def get_default_mailboxes(self):
        return self.mailbox_repo.get_default_mailboxes()

    def get_user_mailboxes(self, user_id):
        return self.mailbox_repo.get_user_mailboxes(user_id)

    def get_all_mailboxes(self, user_id):
        default_mailboxes = self.get_default_mailboxes()
        users_mailboxes = self.get_user_mailboxes(user_id)

        def_mailboxes = []
        for mailbox in default_mailboxes:
            def_mailboxes.append({'mailbox_id': mailbox.id, 'mailbox_name': mailbox.mailbox_name})

        usr_mailboxes = []
        for mailbox in users_mailboxes:
            usr_mailboxes.append({'mailbox_id': mailbox.id, 'mailbox_name': mailbox.mailbox_name})

        mailboxes = {
            'default_mailboxes': def_mailboxes,
            'users_mailboxes': usr_mailboxes
        }
        return mailboxes
