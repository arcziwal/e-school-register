from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import AddStudentForm, CreateStudentAccountForm, AddTeacherForm, CreateTeacherAccountForm, \
    CreateSchoolClassForm, CreateSubjectForm, CreateLessonForm, AssignStudentToClassForm
from .models import Parent, Student, Teacher, SchoolClass, Subject, Lesson, Attendance, Grades
from .scripts import password_generator, get_related_person, get_class_and_subject


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


class Logout(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        logout(request)
        return redirect('/login')


class AddStudentView(LoginRequiredMixin, View):
    login_url = '/login/'

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


class CreateStudentAccountView(LoginRequiredMixin, View):
    login_url = '/login/'

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


class CreateTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'

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


class CreateTeacherAccountView(LoginRequiredMixin, View):
    login_url = '/login/'

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
            return HttpResponse(f"Dodano nauczyciela {first_name} {last_name} <br> login: {login} <br> hasło: {password}")


class CreateSchoolClass(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = CreateSchoolClassForm()
        return render(request, 'create_class_form.html', {'form': form})

    def post(self, request):
        form = CreateSchoolClassForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            tutor = form.cleaned_data['tutor']
            SchoolClass.objects.create(name_of_class=name, tutor=tutor)
            return HttpResponse(f"Klasa {name} została utworzona. Wychowawca: {tutor}")


class CreateSubjectView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = CreateSubjectForm()
        return render(request, 'create_subject_form.html', {'form': form})

    def post(self, request):
        form = CreateSubjectForm(request.POST)
        if form.is_valid():
            type_of_subject = form.cleaned_data['type']
            type_of_subject_display = dict(form.fields['type'].choices)[type_of_subject]
            school_class = form.cleaned_data['school_class']
            teacher = form.cleaned_data['teacher']
            Subject.objects.create(type=type_of_subject, school_class=school_class, teacher=teacher)
            return HttpResponse(f"Przedmiot {type_of_subject_display} dla klasy {school_class} został utworzony."
                                f"Prowadzący: {teacher}")


class CreateLessonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'register_app.can_create_lessons'

    def get(self, request):
        form = CreateLessonForm()
        username = request.user.username
        user = User.objects.get(username=username)
        person, user_type = get_related_person(user)
        return render(request, 'initialize_lesson.html', {'form': form})

    def post(self, request):
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            beginning_hour = form.cleaned_data['beginning_hour']
            ending_hour = form.cleaned_data['ending_hour']
            topic = form.cleaned_data['topic']
            school_class = form.cleaned_data['school_class']
            subject = form.cleaned_data['subject']
            Lesson.objects.create(
                beginning_hour=beginning_hour,
                ending_hour=ending_hour,
                topic=topic,
                school_class=school_class,
                subject=subject
            )
            lesson = Lesson.objects.get(beginning_hour=beginning_hour)
            return redirect(f'/class/{school_class}/{subject}/{lesson}')
        else:
            return render(request, 'initialize_lesson.html', {'form': form})


class AssignStudentToClass(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = AssignStudentToClassForm()
        return render(request, 'assign_student_to_class.html', {'form': form})

    def post(self, request):
        form = AssignStudentToClassForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            school_class = form.cleaned_data['school_class']
            student.school_class = school_class
            student.save()
            return HttpResponse(f"Uczeń {student} został przypisany do klasy {school_class}")


class PresenceCheckView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'register_app.can_check_attendance'

    def get(self, request, **kwargs):
        school_class, school_class_object, subject, subject_object = get_class_and_subject(**kwargs)
        lesson = kwargs['lesson']
        students_list = school_class_object.student_set.all()
        ctx = {
            'school_class': school_class,
            'subject': subject,
            'lesson': lesson,
            'student_list': students_list,
        }
        return render(request, 'presence_check.html', ctx)

    def post(self, request, **kwargs):
        school_class, school_class_object, subject, subject_object = get_class_and_subject(**kwargs)
        lesson = kwargs['lesson']
        lesson_object = Lesson.objects.get(beginning_hour=lesson)
        students_list = school_class_object.student_set.all()
        presence_list = []
        returned_values = request.POST
        for student in students_list:
            if str(student.pk) in returned_values:
                Attendance.objects.create(
                    student=student,
                    lesson=lesson_object,
                    is_present=True
                )
                presence_list.append(f"{student.first_name} {student.last_name}: obecny")
            else:
                Attendance.objects.create(
                    student=student,
                    lesson=lesson_object,
                    is_present=False
                )
                presence_list.append(f"{student.first_name} {student.last_name}: nieobecny")
        ctx = {
            'presence_list': presence_list,
            'school_class': school_class,
            'subject': subject,
            'lesson': lesson,
        }
        return render(request, 'attendance_list.html', ctx)


class AddGradesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'register_app.can_set_grades'

    def get(self, request, **kwargs):
        school_class, school_class_object, subject, subject_object = get_class_and_subject(**kwargs)
        lesson = kwargs['lesson']
        students_list = school_class_object.student_set.all()
        ctx = {
            'school_class': school_class,
            'subject': subject,
            'lesson': lesson,
            'student_list': students_list,
        }
        return render(request, 'add_grades.html', ctx)

    def post(self, request, **kwargs):
        school_class, school_class_object, subject, subject_object = get_class_and_subject(**kwargs)
        lesson = kwargs['lesson']
        lesson_object = Lesson.objects.get(beginning_hour=lesson)
        students_list = school_class_object.student_set.all()
        grades_list = []
        returned_values = request.POST
        response = []
        for student in students_list:
            grades_list.append(
                [
                    student.pk,
                    returned_values[f"{student.pk} grade"],
                    returned_values[f"{student.pk} description"]
                ]
            )
        for grade in grades_list:
            if grade[1]:
                Grades.objects.create(
                    student=Student.objects.get(pk=grade[0]),
                    lesson=lesson_object,
                    grade=grade[1],
                    description=grade[2]
                )
                student = Student.objects.get(pk=grade[0])
                response.append(f"Uczeń: {student.first_name} {student.last_name}, Ocena: {grade[1]}, Opis: {grade[2]}")
        return render(request, 'added_grades_list.html', {'added_grades': response})


class TemporaryView(View):
    def get(self, request):
        return render(request, 'temporary_view.html')

    def post(self, request):
        print("Zalogowano")







