import random
import string


def password_generator():
    characters = list(string.ascii_letters + string.digits)
    random.shuffle(characters)
    password = []
    for i in range(10):
        password.append(random.choice(characters))
    random.shuffle(password)
    password = ''.join(password)
    return password
