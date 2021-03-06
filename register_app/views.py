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


class IndexPage(View):
    """
    Display a main page, seen after login

    **Context**
    ``request.user.username``
        Required to render template with right options available

    **Template**
    :template: 'register_app/index.html'

    """
    login_url = '/login/'
    redirect_field_name = 'index-view'

    def get(self, request):
        ctx = {}
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, "admin_menu.html")
            username = request.user.username
            user = User.objects.get(username=username)
            person, user_type = get_related_person(user)
            if user_type == 'teacher':
                ctx['navbar_options'] = "teacher"
            elif user_type == 'student':
                ctx['navbar_options'] = 'student'
            ctx['username'] = username
            return render(request, 'index.html', ctx)
        else:
            return redirect("login-view")


class Login(View):
    """
    Display login form

    **Context**
        Form to enter login and password

    **Template**
    :template: 'register_app/login_form.html'
    """

    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login_form.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index-view')


class Logout(LoginRequiredMixin, View):
    """
    Logout View, redirecting to '/login' page
    """

    login_url = '/login/'

    def get(self, request):
        logout(request)
        return redirect('/login')


class AddStudentView(LoginRequiredMixin, View):
    """
    Display a form to add new student to db, requires login

    **Context**
    ``AddStudentForm``
        An instance of :forms: register_app.AddStudentForm

    **Template**
    :template: 'register_app/add_student_form.html'
    """

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
            return HttpResponse(f"Ucze?? {first_name} {last_name} dodany do bazy danych")
        return HttpResponse(f"Nie uda??o si??")


class CreateStudentAccountView(LoginRequiredMixin, View):
    """
    Display a view with form to connect student object with User, require login.

    **context**
    ``CreateStudentAccountForm``
        An instance of :forms: register_app.CreateStudentAccountForm

    **Template**
    :template: 'register_app/student_account_creator.html'
    """
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
            Konto ucznia {first_name} {last_name} zosta??o utworzone.
            LOGIN: {username}
            HAS??O: {password}
            """)


class CreateTeacherView(LoginRequiredMixin, View):
    """
    Display a form to create new Teacher in db, require login

    **context**
    ``AddTeacherForm``
        An instance of :forms: register_app.AddTeacherForm

    **Template**
    :template: 'register_app/add_teacher_form.html'
    """
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
            return HttpResponse(f"Nauczyciel: {first_name} {last_name} zosta?? dodany do bazy danych")


class CreateTeacherAccountView(LoginRequiredMixin, View):
    """
    Display a form to connect Teacher object with User object, require login

    **context**
    ``CreateTeacherAccountForm``
        An instance of :forms: register_app.CreateTeacherAccountForm

    **Template**
    :template: 'register_app/teacher_account_creator.html'
    """
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
            return HttpResponse(f"Dodano nauczyciela {first_name} {last_name} <br> login: {login} <br> has??o: {password}")


class CreateSchoolClass(LoginRequiredMixin, View):
    """
    Display a form to create new class in school, require login.

    **context**
    ``CreateSchoolClassForm``
        An instance of :forms: register_app.CreateSchoolClassForm

    **Template**
    :template: 'register_app/create_class_form.html'
    """
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
            return HttpResponse(f"Klasa {name} zosta??a utworzona. Wychowawca: {tutor}")


class CreateSubjectView(LoginRequiredMixin, View):
    """
    Display a from to create new subject in certain class, require login.

    **context**
    ``CreateSubjectForm``
        An instance of :forms: register_app.CreateSubjectForm

    **Template**
    :template: 'register_app/create_subject_form.html'
    """
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
            return HttpResponse(f"Przedmiot {type_of_subject_display} dla klasy {school_class} zosta?? utworzony."
                                f"Prowadz??cy: {teacher}")


class CreateLessonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Display a form to start a new lessons, require login and permissions given to group: Teachers

    **context**
    ``CreateLessonForm``
        An instance of :forms: register_app.CreateLessonForm

    **Template**
    :template: 'register_app/initialize_lesson.html'
    """

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
    """
    Display a form to assign a student to certain class.

    **context**
    ``AssignStudentToClassForm``
        An instance of :forms: register_app.AssignStudentToClassForm

    **Template**
    :template: 'register_app/assign_student_to_class.html'
    """

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
            return HttpResponse(f"Ucze?? {student} zosta?? przypisany do klasy {school_class}")


class PresenceCheckView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Display a form to enter presence on certain lesson.

    :param str school_class: name of class
    :param str subject: name of subject
    :param str lesson: beginning date of certain lesson

    **context**
        Parameters given in request

    **Template**
    :template: 'register_app/presence_check.html'

    """
    login_url = '/login/'
    permission_required = 'register_app.can_create_lessons'

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
    """
    Display a form to enter grades on certain lesson.

    :param str school_class: name of class
    :param str subject: name of subject
    :param str lesson: beginning date of certain lesson

    **context**
        Parameters given in request

    **Template**
    :template: 'register_app/add_grades.html'
    """

    login_url = '/login/'
    permission_required = 'register_app.can_create_lessons'

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
                response.append(f"Ucze??: {student.first_name} {student.last_name}, Ocena: {grade[1]}, Opis: {grade[2]}")
        return render(request, 'added_grades_list.html', {'added_grades': response})


class ShowGradesView(LoginRequiredMixin, View):
    """
       Display a view showing grades of cerain student

       **context**


       **Template**
       :template: 'register_app/
       """

    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            user = User.objects.get(username=username)
            person, user_type = get_related_person(user)
            if user_type == "student":
                students_grades = person.grades_set.all()
                ctx = {
                    'students_grades': students_grades,
                    'student_name': f"{person.first_name} {person.last_name}"
                }
                return render(request, 'show_grades.html', ctx)


class TemporaryView(View):
    """
    Temporary view displayed on subpages under construction

    **Template**
    :template: 'register_app/temporary_view.html'
    """

    def get(self, request):
        return render(request, 'temporary_view.html')

    def post(self, request):
        print("Zalogowano")
