from django.db import models
from django.contrib.auth.models import User


class Parent(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)


class Student(models.Model):
    first_name = models.CharField(max_length=32)
    second_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField()
    create_date = models.DateField(auto_now_add=True)
    pesel = models.CharField(max_length=11)
    address = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=32, null=True)
    zip_code = models.CharField(max_length=6, null=True)
    parents = models.ManyToManyField(Parent)
    school_class = models.ForeignKey('SchoolClass', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)


class SchoolClass(models.Model):
    pass
