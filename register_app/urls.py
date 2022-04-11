from django.urls import path, include
from .views import TemporaryView, IndexPage, Login, RegisterView, AddStudentView, CreateStudentAccountView, \
    CreateTeacherView, CreateTeacherAccountView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", IndexPage.as_view(), name="index-view"),
    path("login/", Login.as_view(), name="login-view"),
    path('register/', RegisterView.as_view(), name="register-view"),
    path('student/add/', AddStudentView.as_view(), name="new-student"),
    path('student/create_account/', CreateStudentAccountView.as_view(), name="create-student-account"),
    path('teacher/add/', CreateTeacherView.as_view(), name="create-teacher"),
    path('teacher/create_account/', CreateTeacherAccountView.as_view(), name="create-teacher-account"),
    path('temp/', TemporaryView.as_view(), name="temporary-view"),
]
