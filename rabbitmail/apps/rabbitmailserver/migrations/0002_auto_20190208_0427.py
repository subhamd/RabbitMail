# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-02-07 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabbitmailserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultmailbox',
            name='mailbox_name',
            field=models.CharField(choices=[('INBOX', 'Inbox'), ('SENT ITEMS', 'Sent Items'), ('DRAFT', 'Draft'), ('TRASH', 'Trash')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='mailcontent',
            name='send_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
