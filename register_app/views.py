from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .forms import AddStudentForm, CreateStudentAccountForm, AddTeacherForm, CreateTeacherAccountForm
from .models import Parent, Student, Teacher
from .scripts import password_generator, get_related_person


class IndexPage(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'index-view'

    def get(self, request):
        ctx = {'nav_bar_elements': [{'href': 'login/', 'name': 'Logowanie'},
                                    {'href': 'register/', 'name': 'Utwórz konto'}
                                    ]}
        if request.user.is_authenticated:
            username = request.user.username
            user = User.objects.get(username=username)
            person, user_type = get_related_person(user)
            print(person.first_name)
            print(user_type)
            ctx['username'] = username
        return render(request, 'index.html', ctx)


class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login_form.html', {'form': form})

    def post(self, request):
        print("przesłano dane")
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print("sprawdzono dane")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print("Wykonano autentyfikację")
            if user is not None:
                login(request, user)
                print("Zalogowano")
                return redirect('index-view')


class RegisterView(View):
    def get(self, request):
        return render(request, 'login_form.html')


class AddStudentView(View):
    def get(self, request):
        form = AddStudentForm()
        return render(request, 'add_student_form.html', {'form': form})

    def post(self, request):
        form = AddStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            second_name = form.cleaned_data['second_name']
            last_name = form.cleaned_data['last_name']
            birth_date = form.cleaned_data['birth_date']
            pesel = form.cleaned_data['pesel']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']
            mother_first_name = request.POST['mother_first_name']
            mother_last_name = request.POST['mother_last_name']
            father_first_name = request.POST['father_first_name']
            father_last_name = request.POST['father_last_name']
            mother = Parent.objects.create(first_name=mother_first_name, last_name=mother_last_name)
            father = Parent.objects.create(first_name=father_first_name, last_name=father_last_name)
            student = Student.objects.create(
                first_name=first_name,
                second_name=second_name,
                last_name=last_name,
                birth_date=birth_date,
                pesel=pesel,
                address=address,
                city=city,
                zip_code=zip_code,
            )
            student.parents.add(mother, father)
            return HttpResponse(f"Uczeń {first_name} {last_name} dodany do bazy danych")
        return HttpResponse(f"Nie udało się")


class CreateStudentAccountView(View):
    def get(self, request):
        form = CreateStudentAccountForm()
        return render(request, 'student_account_creator.html', {'form': form})

    def post(self, request):
        form = CreateStudentAccountForm(request.POST)
        if form.is_valid():
            student_to_add = form.cleaned_data['student']
            first_name = student_to_add.first_name
            last_name = student_to_add.last_name
            username = student_to_add.pesel
            password = password_generator()
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password
            )
            user.save()
            student_to_add.user = user
            student_to_add.save()
            return HttpResponse(f"""
            Konto ucznia {first_name} {last_name} zostało utworzone.
            LOGIN: {username}
            HASŁO: {password}
            """)


class CreateTeacherView(View):
    def get(self, request):
        form = AddTeacherForm()
        return render(request, "add_teacher_form.html", {'form': form})

    def post(self, request):
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            Teacher.objects.create(first_name=first_name, last_name=last_name)
            return HttpResponse(f"Nauczyciel: {first_name} {last_name} został dodany do bazy danych")


class CreateTeacherAccountView(View):
    def get(self, request):
        form = CreateTeacherAccountForm()
        return render(request, 'teacher_account_creator.html', {'form': form})

    def post(self, request):
        form = CreateTeacherAccountForm(request.POST)
        if form.is_valid():
            teacher_to_add = form.cleaned_data['teacher']
            first_name = teacher_to_add.first_name
            last_name = teacher_to_add.last_name
            login = (first_name + '_' + last_name).lower()
            password = password_generator()
            user = User.objects.create_user(
                username=login,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()
            teacher_to_add.user = user
            teacher_to_add.save()
        return HttpResponse("Dodano")


class TemporaryView(View):
    def get(self, request):
        return render(request, 'temporary_view.html')

    def post(self, request):
        print("Zalogowano")







