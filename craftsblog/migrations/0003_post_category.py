# Generated by Django 3.2.20 on 2023-08-20 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('craftsblog', '0002_auto_20230820_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.IntegerField(choices=[(0, 'Books'), (1, 'Lamps'), (2, 'Interior'), (3, 'Other')], default=3),
        ),
    ]