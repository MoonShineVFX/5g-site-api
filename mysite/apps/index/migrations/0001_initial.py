# Generated by Django 3.2.7 on 2021-09-23 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('image', models.ImageField(null=True, upload_to='banners')),
                ('priority', models.ImageField(default=1, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.CharField(max_length=80)),
                ('link', models.URLField()),
                ('image', models.ImageField(null=True, upload_to='partners')),
                ('tag', models.ManyToManyField(to='tag.Tag')),
            ],
        ),
    ]