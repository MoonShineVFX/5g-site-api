# Generated by Django 3.2.7 on 2021-11-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_change_about_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='name_english',
            field=models.CharField(max_length=100, null=True),
        ),
    ]