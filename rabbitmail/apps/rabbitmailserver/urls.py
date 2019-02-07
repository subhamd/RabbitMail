from django.conf.urls import url

from apps.rabbitmailserver.api.create_user import CreateUser
from apps.rabbitmailserver.api.forward_email import ForwardEmail
from apps.rabbitmailserver.api.get_mailboxes import GetMailboxes
from apps.rabbitmailserver.api.get_user_mailbox_emails import GetUserMailboxEmails
from apps.rabbitmailserver.api.save_composed_email import SaveComposedEmail
from apps.rabbitmailserver.api.send_email import SendEmail
from apps.rabbitmailserver.api.view_email import ViewEmail

app_name = 'rabbitmailserver'

urlpatterns = [
    url(r'^mail/compose/$', SaveComposedEmail.as_view(), name='save-composed-mail'),
    url(r'^mail/(?P<mail_id>\d+)/$', ViewEmail.as_view(), name='view-mail'),
    url(r'^mail/(?P<mail_id>\d+)/send/$', SendEmail.as_view(), name='send-mail'),
    url(r'^mail/(?P<mail_id>\d+)/forward/$', ForwardEmail.as_view(), name='forward-mail'),
    url(r'^user/create/$', CreateUser.as_view(), name='create-user'),
    url(r'^user/(?P<user_id>\d+)/mailbox/$', GetMailboxes.as_view(), name='get-user-mailboxes'),
    url(r'^user/(?P<user_id>\d+)/mailbox/(?P<mailbox_id>\d+)/$',
        GetUserMailboxEmails.as_view(), name='get-user-mailbox-mails'),
]
