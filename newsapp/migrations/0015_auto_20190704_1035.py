# Generated by Django 2.2.3 on 2019-07-04 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0014_auto_20190702_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='admin'),
        ),
        migrations.AlterField(
            model_name='editor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='editor'),
        ),
    ]