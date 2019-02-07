from apps.rabbitmailserver.models import MailContent, User
from apps.rabbitmailserver.repositories.mail_content_repository import MailContentRepository
from apps.rabbitmailserver.repositories.user_repo import UserRepository


class MailContentService:
    user_repo = UserRepository()
    mail_content_repo = MailContentRepository()

    def add_mail_content(self,
                         sender_user_id,
                         recipients=None,
                         subject=None,
                         body=None,
                         associated_mail_id=None):
        """
        add MailContent
        :param sender_user_id: sender's user_id
        :param recipients: recipients of mail
        :param subject: subject of mail
        :param body: body of mail
        :param associated_mail_id: associated MailContent's id
        :return:
        """
        sender = self.user_repo.get_user_by_id(sender_user_id)

        mail_content = MailContent()
        mail_content.sender_email_id = sender.email_id
        mail_content.recipients_email_ids = recipients
        mail_content.subject = subject
        mail_content.body = body

        if body:
            mail_content.body_short_display_text = str(body)[:30]

        if associated_mail_id:
            associated_mail_content = MailContent()
            associated_mail_content.id = associated_mail_id
            mail_content.associated_mail_content = associated_mail_content

        self.mail_content_repo.save_mail_content(mail_content)
        return mail_content
