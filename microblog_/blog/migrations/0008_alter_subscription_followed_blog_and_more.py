# Generated by Django 4.2.1 on 2023-05-30 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='followed_blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_blogs', to=settings.AUTH_USER_MODEL),
        ),
    ]