# Generated by Django 4.2.6 on 2023-10-13 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_remove_activity_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='category',
        ),
    ]
