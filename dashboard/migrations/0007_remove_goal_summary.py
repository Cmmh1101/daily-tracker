# Generated by Django 4.2.6 on 2023-10-17 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_rename_action_items_goal_actions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='summary',
        ),
    ]