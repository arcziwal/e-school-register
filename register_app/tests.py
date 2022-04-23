import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def client():
    client = Client()
    return client


def test_login_page(client):
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_required(client):
    c = Client()
    u = User.objects.create_user(username="test_user", password="test")
    c.login(username="test_user", password="test")
    response = c.get("/student/add/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_student_adding(client):
    c = Client()
    u = User.objects.create_user(username="test_user", password="test")
    c.login(username="test_user", password="test")
    response = c.post("/student/add/", {
        'first_name': 'test_first_name',
        'second_name': 'test_second_name',
        'last_name': 'test_last_name',
        'birth_date': '2000-12-20',
        'pesel': '00000000000',
        'address': 'test_address',
        'city': 'test_city',
        'zip_code': 'test_zip_code',
        'mother_first_name': 'test_mother_first_name',
        'mother_last_name': 'test_mother_last_name',
        'father_first_name': 'test_father_first_name',
        'father_last_name': 'test_father_last_name',
    })
    assert response.status_code == 200




