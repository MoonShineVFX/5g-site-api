# Generated by Django 3.2.7 on 2021-11-30 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0003_change_allow_blank_and_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='amount_quota',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
