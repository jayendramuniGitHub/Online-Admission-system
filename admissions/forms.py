from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
# forms.py
from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
# admissions/forms.py
from django import forms
# admissions/forms.py
from django import forms
from .models import Course, CourseApplication

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']
class CourseApplicationForm(forms.ModelForm):
    class Meta:
        model = CourseApplication
        fields = ['name', 'age', 'dob', 'qualification', 'course'] 


