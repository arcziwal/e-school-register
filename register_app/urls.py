from django.urls import path
from .views import TemporaryView, IndexPage, LoginView, RegisterView

urlpatterns = [
    path("", IndexPage.as_view(), name="index-view"),
    path("login/", LoginView.as_view(), name="login-view"),
    path('register/', RegisterView.as_view(), name="register-view")
]
