import datetime

from apps.rabbitmailserver.exceptions.exception import MailAlreadySentException
from apps.rabbitmailserver.models import UserMailboxContent, DefaultMailbox
from apps.rabbitmailserver.repositories.user_mailbox_content_repository import UserMailboxContentRepository
from apps.rabbitmailserver.services.mail_content_service import MailContentService
from apps.rabbitmailserver.services.mailbox_service import MailboxService
from apps.rabbitmailserver.services.user_service import UserService


class UserMailboxContentService:
    user_mailbox_content_repo = UserMailboxContentRepository()
    mailbox_service = MailboxService()
    mail_content_service = MailContentService()
    user_service = UserService()

    def add_user_mailbox_content(self, user, mail_content):
        draft_mailbox = self.mailbox_service.get_default_mailbox_by_name(DefaultMailbox.DRAFT)

        user_mailbox_content = UserMailboxContent()
        user_mailbox_content.user = user
        user_mailbox_content.mail_content = mail_content
        user_mailbox_content.default_mailbox = draft_mailbox

        self.user_mailbox_content_repo.save_user_mailbox_content(user_mailbox_content)
        return user_mailbox_content

    def get_user_mailbox_content_by_id(self, user_mailbox_content_id):
        return self.user_mailbox_content_repo.get_user_mailbox_content_by_id(user_mailbox_content_id)

    def save_user_mailbox_content(self, save_user_mailbox_content):
        self.user_mailbox_content_repo.save_user_mailbox_content(save_user_mailbox_content)

    def get_default_mailbox_mails(self, user_id, mailbox_id):
        default_mailbox = self.mailbox_service.get_default_mailbox_by_id(mailbox_id)

        user_mailbox_contents = self.user_mailbox_content_repo.\
            get_user_mailbox_content_by_user_id_and_default_mailbox_id(user_id, mailbox_id)

        mails = self.__get_mails_from_user_mailbox_contents(user_mailbox_contents, default_mailbox.mailbox_name)
        return mails

    def get_user_defined_mailbox_mails(self, user_id, mailbox_id):
        user_mailbox_contents = self.user_mailbox_content_repo.\
            get_user_mailbox_content_by_user_id_and_user_defined_mailbox_id(user_id, mailbox_id)

        mails = self.__get_mails_from_user_mailbox_contents(user_mailbox_contents)
        return mails

    def get_mail_details(self, user_mailbox_content_id):
        user_mailbox_content = self.get_user_mailbox_content_by_id(user_mailbox_content_id)

        mail_details = self.__create_mail_details(user_mailbox_content.id, user_mailbox_content.user.id,
                                                  user_mailbox_content.mail_content)
        return mail_details

    def send_mail(self, user_mailbox_content):
        mail_content = user_mailbox_content.mail_content
        if mail_content.send_at:
            raise MailAlreadySentException()

        sent_mailbox = self.mailbox_service.get_default_mailbox_by_name(DefaultMailbox.SENT_ITEMS)

        # update user_mailbox_content from DRAFT to SENT ITEMS
        user_mailbox_content.default_mailbox = sent_mailbox
        self.user_mailbox_content_repo.save_user_mailbox_content(user_mailbox_content)

        # add user_mailbox_content for internal recipients (recipients in system)
        recipients = mail_content.recipients_email_ids.split(';')
        send_to_users = self.user_service.get_users_by_email_ids(recipients)
        inbox_mailbox = self.mailbox_service.get_default_mailbox_by_name(DefaultMailbox.INBOX)
        for send_to_user in send_to_users:
            user_mailbox_content = UserMailboxContent()
            user_mailbox_content.default_mailbox = inbox_mailbox
            user_mailbox_content.mail_content = mail_content
            user_mailbox_content.user = send_to_user
            user_mailbox_content.is_read = False
            self.user_mailbox_content_repo.save_user_mailbox_content(user_mailbox_content)

        # send mail to external recipients
        internal_recipients, external_recipients = self.__get_external_recipients(recipients, send_to_users)
        self.mailbox_service.send_mail_to_external_recipients(external_recipients)

        # update send_at for mail_content
        mail_content.send_at = datetime.datetime.now()
        self.mail_content_service.save_mail_content(mail_content)

        return internal_recipients, external_recipients

    def delete_email_to_trash(self, user_mailbox_content_id):
        user_mailbox_content = self.get_user_mailbox_content_by_id(user_mailbox_content_id)

        if user_mailbox_content.default_mailbox.mailbox_name == DefaultMailbox.TRASH:
            raise Exception()

        trash_mailbox = self.mailbox_service.get_default_mailbox_by_name(DefaultMailbox.TRASH)
        user_mailbox_content.default_mailbox = trash_mailbox

        self.save_user_mailbox_content(user_mailbox_content)

    def __get_mails_from_user_mailbox_contents(self, user_mailbox_contents, mailbox_name=None):
        all_mails = []
        read_mails = []
        unread_mails = []

        for user_mailbox_content in user_mailbox_contents:
            mail_content = user_mailbox_content.mail_content
            email_content = {
                'mail_id': user_mailbox_content.id,
                'subject': mail_content.subject if mail_content.subject else '(no subject)',
                'body_display_text': mail_content.body_short_display_text
            }

            if mailbox_name == DefaultMailbox.DRAFT:
                email_content['drafted_at'] = mail_content.modified_at
                email_content['to'] = 'Draft'
            else:
                email_content['sent_at'] = mail_content.send_at
                if mailbox_name == DefaultMailbox.SENT_ITEMS:
                    recipients = mail_content.recipients_email_ids.split(';')
                    email_content['to'] = recipients if len(recipients) == 1 else (recipients[0] + ' ...')
                else:
                    email_content['from'] = mail_content.sender_email_id

            if mailbox_name != DefaultMailbox.INBOX:
                all_mails.append(email_content)
            elif user_mailbox_content.is_read:
                read_mails.append(email_content)
            else:
                unread_mails.append(email_content)

        if mailbox_name == DefaultMailbox.INBOX:
            mails = {
                'read_mails': read_mails,
                'unread_mails': unread_mails
            }
        else:
            mails = {
                'all_mails': all_mails
            }

        return mails

    def __get_external_recipients(self, recipients, send_to_users):
        internal_recipients = []
        for user in send_to_users:
            internal_recipients.append(user.email_id)

        external_recipients = []
        for recipient in recipients:
            if recipient not in internal_recipients:
                external_recipients.append(recipient)

        return internal_recipients, external_recipients

    def __create_mail_details(self, user_mailbox_content_id, user_id, mail_content):
        mail_details = {
            'id': user_mailbox_content_id,
            'from': mail_content.sender_email_id,
            'to': mail_content.recipients_email_ids,
            'subject': mail_content.subject,
            'body': mail_content.body,
        }

        if mail_content.send_at:
            mail_details['sent_at'] = mail_content.send_at
        else:
            mail_details['last_modified_at'] = mail_content.modified_at

        if mail_content.associated_mail_content:
            user_mailbox_content = self.user_mailbox_content_repo\
                    .get_user_mailbox_content_by_user_id_and_mail_content_id(user_id,
                                                                             mail_content.associated_mail_content.id)

            mail_details['associated_mail'] = self.__create_mail_details(user_mailbox_content.id, user_id,
                                                                         mail_content.associated_mail_content)

        return mail_details
