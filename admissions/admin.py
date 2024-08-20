from django.contrib import admin
from .models import Course, Student, CourseApplication, Notification

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(CourseApplication)
admin.site.register(Notification)
