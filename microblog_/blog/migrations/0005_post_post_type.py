# Generated by Django 4.2.1 on 2023-05-28 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_like_options_alter_like_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('personal', 'Личный пост'), ('teacher', 'Преподавательский пост'), ('group', 'Пост учебной группы'), ('admin', 'Административный пост')], default='personal', max_length=10),
            preserve_default=False,
        ),
    ]
