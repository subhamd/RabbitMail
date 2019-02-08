from apps.rabbitmailserver.repositories.mailbox_repository import MailboxRepository


class MailboxService:
    mailbox_repo = MailboxRepository()

    def get_default_mailboxes(self):
        return self.mailbox_repo.get_default_mailboxes()

    def get_default_mailbox_by_name(self, mailbox_name):
        return self.mailbox_repo.get_default_mailbox_by_name(mailbox_name)

    def get_default_mailbox_by_id(self, mailbox_id):
        return self.mailbox_repo.get_default_mailbox_by_id(mailbox_id)

    def get_user_defined_mailboxes(self, user_id):
        return self.mailbox_repo.get_user_defined_mailboxes(user_id)

    def get_all_mailboxes(self, user_id):
        default_mailboxes = self.get_default_mailboxes()
        user_defined_mailboxes = self.get_user_defined_mailboxes(user_id)

        def_mailboxes = []
        for mailbox in default_mailboxes:
            def_mailboxes.append({'mailbox_id': mailbox.id, 'mailbox_name': mailbox.mailbox_name})

        usr_mailboxes = []
        for mailbox in user_defined_mailboxes:
            usr_mailboxes.append({'mailbox_id': mailbox.id, 'mailbox_name': mailbox.mailbox_name})

        mailboxes = {
            'default_mailboxes': def_mailboxes,
            'user_defined_mailboxes': usr_mailboxes
        }
        return mailboxes

    def send_mail_to_external_recipients(self, external_recipients):
        pass
