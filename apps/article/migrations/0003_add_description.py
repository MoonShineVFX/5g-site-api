# Generated by Django 3.2.7 on 2021-10-04 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='description',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]