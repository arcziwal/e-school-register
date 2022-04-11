# Generated by Django 4.0.3 on 2022-03-14 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=64)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('second_name', models.CharField(max_length=32, null=True)),
                ('last_name', models.CharField(max_length=64)),
                ('birth_date', models.DateField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('pesel', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=32, null=True)),
                ('city', models.CharField(max_length=32, null=True)),
                ('zip_code', models.CharField(max_length=6, null=True)),
                ('parents', models.ManyToManyField(to='register_app.parent')),
                ('school_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='register_app.schoolclass')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
