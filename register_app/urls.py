from django.urls import path
from .views import TemporaryView

urlpatterns = [
    path("", TemporaryView.as_view(), name="temporary-view"),
]