# Generated by Django 2.2.2 on 2019-07-01 14:02

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0005_news_admin'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='news',
            managers=[
                ('verified', django.db.models.manager.Manager()),
            ],
        ),
    ]
