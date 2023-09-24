# Generated by Django 3.2 on 2023-09-24 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_rename_title_todo_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='complete',
            field=models.CharField(choices=[('complete', 'complete'), ('pending', 'pending')], default='pending', max_length=8),
        ),
    ]
