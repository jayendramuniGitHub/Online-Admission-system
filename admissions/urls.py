# online_admission/urls.py
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from admissions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/student/login/')),
    path('student/login/', views.student_login, name='student_login'),
    path('head/login/', views.admin_login, name='admin_login'),
    path('signup/', views.signup, name='signup'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('head/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('head/manage_applications/', views.manage_applications, name='manage_applications'),
    path('head/manage_applications/<int:application_id>/', views.manage_applications, name='manage_application_by_id'),
]
