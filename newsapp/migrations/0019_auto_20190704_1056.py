# Generated by Django 2.2.3 on 2019-07-04 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0018_auto_20190704_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='team/admin/'),
        ),
        migrations.AlterField(
            model_name='editor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='team/editor/'),
        ),
    ]
