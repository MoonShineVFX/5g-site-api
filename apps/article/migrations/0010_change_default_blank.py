# Generated by Django 3.2.7 on 2021-10-12 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_change_allow_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='news',
            name='detail',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
