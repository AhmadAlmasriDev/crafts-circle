# Generated by Django 3.2.20 on 2023-08-20 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('craftsblog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='comment_body',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='body',
            new_name='message_body',
        ),
    ]
