from django.db import models
from django.contrib.auth.models import User

SUBCJECTS = [
    (1, 'Biologia'),
    (2, 'Geografia'),
    (3, 'Fizyka'),
    (4, 'Chemia'),
    (5, 'Matematyka'),
    (6, 'Język Polski'),
    (7, 'Język angielski'),
]


class Parent(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    first_name = models.CharField('Imię (imiona)', max_length=32)
    last_name = models.CharField('Nazwisko', max_length=64)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    class Meta:

        permissions = (
            ("can_create_lessons", "Provides possibility to create new lessons"),
            ("can_set_attendance", "Provides possibility to check attendance"),
            ("can_set_grades", "Provides possibility to set grades"),
            ('can_view_grades', "Can view grades"),
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SchoolClass(models.Model):
    name_of_class = models.CharField(verbose_name='symbol', max_length=2, default="NIEPRZYPISANE")
    tutor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name="wychowawca")

    def __str__(self):
        return self.name_of_class


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
    school_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    class Meta:

        permissions = (
            ('can_view_grades', 'can view grades'),
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}, PESEL: {self.pesel}"


class Subject(models.Model):
    type = models.IntegerField(choices=SUBCJECTS, default='nieprzypisane')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default='nieprzypisany')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_type_display()


class Lesson(models.Model):
    beginning_hour = models.DateTimeField()
    ending_hour = models.DateTimeField()
    topic = models.CharField(max_length=64)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.beginning_hour}"


class Grades(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    description = models.CharField(max_length=32)


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_present = models.BooleanField()







