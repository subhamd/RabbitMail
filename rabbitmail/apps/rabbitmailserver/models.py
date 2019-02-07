from django.db import models
from djutil.models import TimeStampedModel


class DefaultMailbox(models.Model):
    INBOX = 'INBOX'
    SENT_ITEMS = 'SENT ITEMS'
    DRAFT = 'DRAFT'
    TRASH = 'TRASH'

    MAILBOX_NAME = (
        (INBOX, 'Inbox'),
        (SENT_ITEMS, 'Sent Items'),
        (DRAFT, 'Draft'),
        (TRASH, 'Trash')
    )

    mailbox_name = models.CharField(
        max_length=20,
        choices=MAILBOX_NAME,
        unique=True,
        null=False,
        blank=False
    )


class MailContent(TimeStampedModel):
    sender_email_id = models.CharField(max_length=50, null=True, blank=True)
    recipients_email_ids = models.CharField(max_length=500, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    body = models.CharField(max_length=100, null=True, blank=True)
    body_short_display_text = models.CharField(max_length=30, null=True, blank=True)
    send_at = models.DateTimeField(db_index=True, null=True, blank=True)
    associated_mail_content = models.ForeignKey(
        'MailContent',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=False,
    )


def mail_content_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/mail_content_<id>/<filename>
    return 'mail_content_{0}/{1}'.format(instance.mail_content.id, filename)


class Attachment(models.Model):
    mail_content = models.ForeignKey(
        'MailContent',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    attachment = models.FileField(upload_to=mail_content_directory_path)


class User(TimeStampedModel):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=False, blank=False, db_index=True)


class UserDefinedMailbox(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    mailbox_name = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )


class UserMailboxContent(TimeStampedModel):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    mail_content = models.ForeignKey(
        'MailContent',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        db_index=False,
    )
    default_mailbox = models.ForeignKey(
        'DefaultMailbox',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_defined_mailbox = models.ForeignKey(
        'UserDefinedMailbox',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    is_read = models.NullBooleanField()
