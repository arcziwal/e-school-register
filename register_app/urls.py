from django.urls import path, include
from .views import TemporaryView, IndexPage, Login, Logout, AddStudentView, CreateStudentAccountView, \
    CreateTeacherView, CreateTeacherAccountView, CreateSchoolClass, CreateSubjectView, CreateLessonView, \
    PresenceCheckView, AssignStudentToClass, AddGradesView, ShowGradesView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", IndexPage.as_view(), name="index-view"),
    path("login/", Login.as_view(), name="login-view"),
    path("logout/", Logout.as_view(), name='logout-view'),
    path('student/add/', AddStudentView.as_view(), name="new-student"),
    path('student/create_account/', CreateStudentAccountView.as_view(), name="create-student-account"),
    path('teacher/add/', CreateTeacherView.as_view(), name="create-teacher"),
    path('teacher/create_account/', CreateTeacherAccountView.as_view(), name="create-teacher-account"),
    path('class/create/', CreateSchoolClass.as_view(), name='create-class'),
    path('class/subject/create', CreateSubjectView.as_view(), name='create-subject'),
    path('class/subject/lesson/init', CreateLessonView.as_view(), name='initialize-lesson'),
    path('student/assign_to_class', AssignStudentToClass.as_view(), name='assign-student-to-class'),
    path('class/<str:school_class>/<str:subject>/<str:lesson>', PresenceCheckView.as_view(), name='check-presence'),
    path('class/<str:school_class>/<str:subject>/<str:lesson>/grades', AddGradesView.as_view(), name='add-grades'),
    path('student/show_grades', ShowGradesView.as_view(), name="show=grades"),
    path('temp/', TemporaryView.as_view(), name="temporary-view"),
]
