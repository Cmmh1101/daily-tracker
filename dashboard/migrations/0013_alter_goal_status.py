# Generated by Django 4.2.6 on 2023-11-09 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_goal_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='status',
            field=models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Achieved', 'Achieved')], default='Not Started', max_length=20),
        ),
    ]
