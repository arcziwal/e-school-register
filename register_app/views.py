from django.shortcuts import render
from django.views import View


class TemporaryView(View):
    def get(self, request):
        return render(request, '__base__.html')
