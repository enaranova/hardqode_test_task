# Generated by Django 4.2.5 on 2024-03-02 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_rename_title_lesson_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='video_link',
            new_name='video_url',
        ),
    ]