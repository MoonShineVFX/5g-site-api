# Generated by Django 3.2.7 on 2021-09-30 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_rename_to_banner_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField(null=True)),
            ],
        ),
    ]
