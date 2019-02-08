from apps.rabbitmailserver.exceptions.exception import InvalidMailContentIdException
from apps.rabbitmailserver.models import MailContent


class MailContentRepository:

    def save_mail_content(self, mail_content):
        mail_content.save()

    def get_mail_content_by_id(self, mail_content_id):
        try:
            mail_content = MailContent.objects.get(pk=mail_content_id)
            return mail_content
        except MailContent.DoesNotExist:
            raise InvalidMailContentIdException("Email with mail_id: {0} doesn't exist".format(mail_content_id))

