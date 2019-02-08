from apps.rabbitmailserver.models import MailContent
from apps.rabbitmailserver.repositories.mail_content_repository import MailContentRepository


class MailContentService:
    mail_content_repo = MailContentRepository()

    def add_mail_content(self,
                         sender,
                         recipients=None,
                         subject=None,
                         body=None,
                         associated_mail_id=None):
        """
        add MailContent
        :param apps.rabbitmailserver.models.User sender:
        :param recipients: recipients of mail
        :param subject: subject of mail
        :param body: body of mail
        :param associated_mail_id: associated MailContent's id
        :return:
        """

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

        self.save_mail_content(mail_content)
        return mail_content

    def save_mail_content(self, mail_content):
        self.mail_content_repo.save_mail_content(mail_content)

    def get_mail_content_by_id(self, mail_content_id):
        mail_content = self.mail_content_repo.get_mail_content_by_id(mail_content_id)
        return mail_content
