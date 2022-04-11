from django.forms import ModelForm
from .models import Student, Teacher
from django import forms

YEARS = (2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016)


class AddStudentForm(ModelForm):

    second_name = forms.CharField(required=False)
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)

    class Meta:
        model = Student
        exclude = ['create_date', 'school_class', 'user', 'parents']
        widgets = {
            'birth_date': forms.SelectDateWidget(years=YEARS, attrs=({'style': 'width: 33%; display: inline-block;'})),
            'pesel': forms.TextInput(attrs={'size': 11, 'title': 'numer PESEL', 'style': 'max-width: 9em'})

        }


class CreateStudentAccountForm(ModelForm):

    student = forms.ModelChoiceField(queryset=Student.objects.filter(user=None), initial=0)

    class Meta:
        model = Student
        fields = {'student'}


class AddTeacherForm(ModelForm):

    class Meta:
        model = Teacher
        exclude = ['user']


class CreateTeacherAccountForm(ModelForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.filter(user=None), initial=0)

    class Meta:
        model = Teacher
        fields = {'teacher'}
