# Generated by Django 4.2.1 on 2023-05-28 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('personal', 'personal'), ('teacher', 'teacher'), ('group', 'group'), ('admin', 'admin')], max_length=10),
        ),
    ]
