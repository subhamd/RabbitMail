from apps.rabbitmailserver.models import UserMailboxContent, User, DefaultMailbox
from apps.rabbitmailserver.repositories.mailbox_repository import MailboxRepository
from apps.rabbitmailserver.repositories.user_mailbox_content_repository import UserMailboxContentRepository


class UserMailboxContentService:
    user_mailbox_content_repo = UserMailboxContentRepository()
    mailbox_repo = MailboxRepository()

    def add_user_mailbox_content(self, user_id, mail_content):
        user_mailbox_content = UserMailboxContent()

        user = User()
        user.id = user_id
        user_mailbox_content.user = user

        user_mailbox_content.mail_content = mail_content

        default_mailbox = self.mailbox_repo.get_default_mailbox_by_name(DefaultMailbox.DRAFT)
        user_mailbox_content.default_mailbox = default_mailbox

        self.user_mailbox_content_repo.save_user_mailbox_content(user_mailbox_content)
