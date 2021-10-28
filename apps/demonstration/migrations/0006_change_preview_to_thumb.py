# Generated by Django 3.2.7 on 2021-10-28 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demonstration', '0005_remove_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demonstration',
            name='preview',
        ),
        migrations.AddField(
            model_name='demonstration',
            name='thumb',
            field=models.ImageField(null=True, upload_to='demonstrations/images'),
        ),
    ]
