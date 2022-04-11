# Generated by Django 4.0.3 on 2022-03-20 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='parents',
        ),
        migrations.AddField(
            model_name='student',
            name='father_first_name',
            field=models.CharField(default=None, max_length=32),
        ),
        migrations.AddField(
            model_name='student',
            name='father_last_name',
            field=models.CharField(default=None, max_length=64),
        ),
        migrations.AddField(
            model_name='student',
            name='mother_first_name',
            field=models.CharField(default=None, max_length=32),
        ),
        migrations.AddField(
            model_name='student',
            name='mother_last_name',
            field=models.CharField(default=None, max_length=64),
        ),
    ]
