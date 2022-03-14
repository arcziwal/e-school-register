from django.shortcuts import render
from django.views import View
from .forms import AddStudentForm
from django.http import HttpResponse


class IndexPage(View):
    def get(self, request):
        ctx = {'nav_bar_elements': [{'href': 'login/', 'name': 'Logowanie'},
                                    {'href': 'register/', 'name': 'Utwórz konto'}
                                    ]}
        return render(request, 'index.html', ctx)


class LoginView(View):
    def get(self, request):
        return render(request, 'login_form.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'login_form.html')


class AddStudentView(View):
    def get(self, request):
        form = AddStudentForm()
        return render(request, 'add_student_form.html', {'form': form})

    def post(self, request):
        return HttpResponse("Dziękuję")


class TemporaryView(View):
    def get(self, request):
        return render(request, '__base__.html')
