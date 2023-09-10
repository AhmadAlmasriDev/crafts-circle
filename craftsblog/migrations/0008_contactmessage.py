# Generated by Django 3.2.20 on 2023-09-07 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('craftsblog', '0007_alter_post_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('user_email', models.EmailField(max_length=254)),
                ('message_body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
    ]