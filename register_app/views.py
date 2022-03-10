from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import UserCreationForm


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
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'login_form.html')



class TemporaryView(View):
    def get(self, request):
        return render(request, '__base__.html')
