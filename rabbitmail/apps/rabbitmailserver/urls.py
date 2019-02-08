from django.conf.urls import url

from apps.rabbitmailserver.api.add_user import AddUser
from apps.rabbitmailserver.api.forward_email import ForwardEmail
from apps.rabbitmailserver.api.get_mailboxes import GetMailboxes
from apps.rabbitmailserver.api.get_user_mailbox_emails import GetUserMailboxEmails
from apps.rabbitmailserver.api.reply_to_email import ReplyToEmail
from apps.rabbitmailserver.api.save_composed_email import SaveComposedEmail
from apps.rabbitmailserver.api.send_email import SendEmail
from apps.rabbitmailserver.api.view_and_delete_email import ViewAndDeleteEmail

app_name = 'rabbitmailserver'

urlpatterns = [
    url(r'^mail/(?P<mail_id>\d+)/$', ViewAndDeleteEmail.as_view(), name='view-mail'),
    url(r'^mail/(?P<mail_id>\d+)/send/$', SendEmail.as_view(), name='send-mail'),
    url(r'^mail/(?P<mail_id>\d+)/forward/$', ForwardEmail.as_view(), name='forward-mail'),
    url(r'^mail/(?P<mail_id>\d+)/reply/$', ReplyToEmail.as_view(), name='reply-to-mail'),
    url(r'^mail/(?P<mail_id>\d+)/$', ViewAndDeleteEmail.as_view(), name='delete-mail'),
    url(r'^user/(?P<user_id>\d+)/mail/compose/$', SaveComposedEmail.as_view(), name='save-composed-mail'),
    url(r'^user/add/$', AddUser.as_view(), name='add-user'),
    url(r'^user/(?P<user_id>\d+)/mailbox/$', GetMailboxes.as_view(), name='get-user-mailboxes'),
    url(r'^user/(?P<user_id>\d+)/mailbox/(?P<mailbox_id>\d+)/$',
        GetUserMailboxEmails.as_view(), name='get-user-mailbox-mails'),
]
