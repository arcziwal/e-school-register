from django.urls import path
from .views import TemporaryView, IndexPage, LoginView

urlpatterns = [
    path("", IndexPage.as_view(), name="temporary-view"),
    path("login/", LoginView.as_view(), name="login-view"),
]
