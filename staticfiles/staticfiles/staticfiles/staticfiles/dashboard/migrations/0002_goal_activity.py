# Generated by Django 4.2.6 on 2023-10-09 03:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('long_term', 'Long Term'), ('mid_term', 'Mid Term'), ('weekly', 'Weekly')], max_length=20)),
                ('summary', models.TextField()),
                ('description', models.TextField()),
                ('action_items', models.TextField()),
                ('category', models.CharField(choices=[('professional', 'Professional'), ('personal', 'Personal'), ('development', 'Development'), ('spiritual', 'Spiritual'), ('faith', 'Faith'), ('charity', 'Charity')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.CharField(choices=[('professional', 'Professional'), ('personal', 'Personal'), ('development', 'Development'), ('ministry', 'Ministry')], max_length=20)),
                ('linked_goals', models.ManyToManyField(related_name='linked_activities', to='dashboard.goal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
