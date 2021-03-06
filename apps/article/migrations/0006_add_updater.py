# Generated by Django 3.2.7 on 2021-10-05 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0005_rename_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='updater',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='article_news_update', to='user.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_news_creation', to=settings.AUTH_USER_MODEL),
        ),
    ]
