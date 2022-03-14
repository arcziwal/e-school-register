from django.forms import ModelForm
from .models import Student


class AddStudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['create_date', 'school_class', 'user']

