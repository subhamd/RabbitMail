# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-02-08 13:04
from __future__ import unicode_literals

import apps.rabbitmailserver.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to=apps.rabbitmailserver.models.mail_content_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultMailbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailbox_name', models.CharField(choices=[('INBOX', 'Inbox'), ('DRAFT', 'Draft'), ('SENT ITEMS', 'Sent Items'), ('TRASH', 'Trash')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('sender_email_id', models.CharField(blank=True, max_length=50, null=True)),
                ('recipients_email_ids', models.CharField(blank=True, max_length=500, null=True)),
                ('subject', models.CharField(blank=True, max_length=100, null=True)),
                ('body', models.CharField(blank=True, max_length=100, null=True)),
                ('body_short_display_text', models.CharField(blank=True, max_length=30, null=True)),
                ('send_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('associated_mail_content', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rabbitmailserver.MailContent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email_id', models.CharField(db_index=True, max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserDefinedMailbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailbox_name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rabbitmailserver.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserMailboxContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_read', models.NullBooleanField()),
                ('default_mailbox', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rabbitmailserver.DefaultMailbox')),
                ('mail_content', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='rabbitmailserver.MailContent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rabbitmailserver.User')),
                ('user_defined_mailbox', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rabbitmailserver.UserDefinedMailbox')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='mail_content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rabbitmailserver.MailContent'),
        ),
    ]
