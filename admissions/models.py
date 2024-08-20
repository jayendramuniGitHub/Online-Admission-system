# admissions/models.py
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, through='CourseApplication')

    def __str__(self):
        return self.user.username

class CourseApplication(models.Model):
    # Your existing fields
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    dob = models.DateField(null=True, blank=True)  # Allow NULL values for dob
    qualification = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    # New field for review status
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.course.title}"

class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.message[:50]}"
