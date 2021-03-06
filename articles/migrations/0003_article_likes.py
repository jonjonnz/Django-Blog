# Generated by Django 3.2.8 on 2021-11-04 07:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0002_alter_article_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(related_name='num_of_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
