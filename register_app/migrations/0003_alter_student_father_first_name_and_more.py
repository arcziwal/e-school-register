# Generated by Django 4.0.3 on 2022-03-20 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_app', '0002_remove_student_parents_student_father_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='father_first_name',
            field=models.CharField(default='undefined', max_length=32),
        ),
        migrations.AlterField(
            model_name='student',
            name='father_last_name',
            field=models.CharField(default='undefined', max_length=64),
        ),
        migrations.AlterField(
            model_name='student',
            name='mother_first_name',
            field=models.CharField(default='undefined', max_length=32),
        ),
        migrations.AlterField(
            model_name='student',
            name='mother_last_name',
            field=models.CharField(default='undefined', max_length=64),
        ),
    ]
