from django.db import models
from django.contrib.auth.models import User

SUBJECTS = [
    (1, 'Biologia'),
    (2, 'Geografia'),
    (3, 'Fizyka'),
    (4, 'Chemia'),
    (5, 'Matematyka'),
    (6, 'Język Polski'),
    (7, 'Język angielski'),
]


class Parent(models.Model):
    """
    Represent a parent of student, related to :model: auth.User
    """
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    """
    Represent a teacher, related to :model: auth.User
    """
    first_name = models.CharField('Imię (imiona)', max_length=32)
    last_name = models.CharField('Nazwisko', max_length=64)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        """
        Permissions given to teachers, like: creating lessons, checking attendance or setting grades
        """

        permissions = (
            ("can_create_lessons", "Provides possibility to create new lessons"),
            ("can_set_attendance", "Provides possibility to check attendance"),
            ("can_set_grades", "Provides possibility to set grades"),
            ('can_view_grades', "Can view grades"),
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SchoolClass(models.Model):
    """
    Represent a single school class, related to :model: register.app.Teacher which represent tutor
    """
    name_of_class = models.CharField(verbose_name='symbol', max_length=2, default="NIEPRZYPISANE")
    tutor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name="wychowawca")

    def __str__(self):
        return self.name_of_class


class Student(models.Model):
    """
    Represent a single student, has relation many-to-many with:
    :model: register_app.Parent which represents parents
    :model: register_app.SchoolClass which represent a class to which student is assigned
    :model: auth.User which represent User account of student
    """

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
        """
        Set of permissions given to Students, like possibility to check its grades.
        """
        permissions = (
            ('can_view_grades', 'can view grades'),
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}, PESEL: {self.pesel}"


class Subject(models.Model):
    """
    Represent single subject of certain school class, is related to:
    :models: register_app.Teacher which represent teacher of particular subject
    :models: register_app.SchoolClass which indicates to which class belongs particular subject
    """

    type = models.IntegerField(choices=SUBJECTS, default='nieprzypisane')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default='nieprzypisany')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_type_display()


class Lesson(models.Model):
    """
    Represents a single lesson, has a beginning and ending time and topic. Is related to:
    :models: register_app.Subject which indicates subject that lesson belongs to
    :models: register_app.SchoolClass which indicates class that lesson belongs to
    """

    beginning_hour = models.DateTimeField()
    ending_hour = models.DateTimeField()
    topic = models.CharField(max_length=64)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.beginning_hour}"


class Grades(models.Model):
    """
    Represents a set of all grades created on particular lesson related to all lecturers of this lesson. Has relations to:
    :models: register_app.Student which indicates student that posses certain grade
    :models: register_app.Lesson which indicates on which lesson grades was set
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    description = models.CharField(max_length=32)


class Attendance(models.Model):
    """
    Represent a set of attendances of all students of certain lesson. Has relations to:
    :models: register_app.Student which indicates student present on lesson
    :models: register_app.Lesson which indicates on which lesson attendance was checked
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_present = models.BooleanField()







