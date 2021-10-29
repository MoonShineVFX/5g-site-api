# Generated by Django 3.2.7 on 2021-10-28 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demonstration', '0007_change_location_url_to_textfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='demonstration',
            name='by_drive',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='demonstration',
            name='by_mrt',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='demonstration',
            name='link',
            field=models.URLField(null=True),
        ),
        migrations.DeleteModel(
            name='Link',
        ),
    ]