import random
import string
from .models import Teacher, Student, Parent


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

