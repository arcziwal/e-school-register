from django.shortcuts import render
from django.views import View


class IndexPage(View):
    def get(self, request):
        ctx = {'nav_bar_elements': [{'href': '#', 'name': 'Logowanie'},
                                    {'href': '#', 'name': 'Utwórz konto'}
                                    ]}
        return render(request, 'index.html', ctx)


class LoginView(View):
    def get(self, request):
        return render(request, 'login_form.html')


class TemporaryView(View):
    def get(self, request):
        return render(request, '__base__.html')
