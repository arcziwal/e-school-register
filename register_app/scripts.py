import random
import string
from .models import Teacher, Student, Parent, SchoolClass, SUBJECTS, Subject


def password_generator():
    characters = list(string.ascii_letters + string.digits)
    random.shuffle(characters)
    password = []
    for i in range(10):
        password.append(random.choice(characters))
    random.shuffle(password)
    password = ''.join(password)
    return password


def get_related_person(user):
    if user is not None:
        if hasattr(user, 'teacher'):
            person = user.teacher
            user_type = "teacher"
        elif hasattr(user, 'student'):
            person = user.student
            user_type = "student"
        elif hasattr(user, 'parent'):
            person = user.parent
            user_type = "parent"
        else:
            person = "unassigned"
            return None
        return person, user_type


def get_class_and_subject(**kwargs):
    school_class = kwargs['school_class']
    subject = kwargs['subject']
    school_class_object = SchoolClass.objects.get(name_of_class=school_class)
    for i in range(len(SUBJECTS)):
        if subject == SUBJECTS[i][1]:
            subject_object = Subject.objects.get(type=SUBJECTS[i][0])
        else:
            subject_object = None
        return school_class, school_class_object, subject, subject_object
    return school_class, school_class_object
