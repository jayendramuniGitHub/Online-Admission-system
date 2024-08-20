from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from .forms import LoginForm, SignUpForm, CourseForm, CourseApplicationForm
from .models import Course, CourseApplication, Student, Notification

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                user = User.objects.create_user(username=username, email=email, password=password)
                student = Student.objects.create(user=user)
                login(request, user)
                return redirect('student_dashboard')
            else:
                error_message = "Passwords do not match."
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')
            else:
                error_message = "Invalid username or password."
                return render(request, 'student_login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'student_login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                error_message = "Invalid username or password or user is not an admin."
                return render(request, 'admin_login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'admin_login.html', {'form': form})

@login_required
def student_dashboard(request):
    # Ensure the student object exists
    try:
        student = request.user.student
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user)

    notifications = Notification.objects.filter(student=student)
    courses = Course.objects.all()

    if request.method == 'POST':
        print("Received a POST request to submit the course application form.")

        form = CourseApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student
            application.save()

            Notification.objects.create(
                student=student,
                message=f"New application submitted for {application.course.title}"
            )

            print("Form data saved successfully:", form.cleaned_data)
            return redirect('student_dashboard')
        else:
            print("Form errors:", form.errors)
    else:
        form = CourseApplicationForm()

    admin_group = get_object_or_404(Group, name='admin')

    return render(request, 'student_dashboard.html', {'courses': courses, 'notifications': notifications, 'form': form})

@login_required
def admin_dashboard(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CourseForm()

    courses = Course.objects.all()
    applications = CourseApplication.objects.all()

    return render(request, 'admin_dashboard.html', {'form': form, 'courses': courses, 'applications': applications})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CourseApplication, Notification

@login_required
def manage_applications(request, application_id=None):
    if not request.user.is_staff:
        return redirect('student_dashboard')

    if application_id:
        applications = CourseApplication.objects.filter(id=application_id)
    else:
        applications = CourseApplication.objects.all()

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')
        application = get_object_or_404(CourseApplication, id=application_id)
        if action == 'accept':
            application.accepted = True
            application.save()
            Notification.objects.create(student=application.student, message=f"Your application for {application.course.title} has been accepted.")
        elif action == 'reject':
            application.delete()  # Delete the application
            Notification.objects.filter(student=application.student, message__icontains=application.course.title).delete()  # Delete the associated notification

        return redirect('admin_dashboard')

    return render(request, 'manage_applications.html', {'applications': applications})