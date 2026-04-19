from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from task.models import Task

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'priority']
        widgets = {
           
            'description': forms.Textarea(attrs={'rows': 5}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }