from django import forms
from .models import Task, User
from django.contrib.auth.forms import UserCreationForm


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"cols": "auto", "rows": 4}),
        initial="",
    )

    class Meta:
        model = Task
        fields = ["name", "description", "priority", "deadline"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class MyUserCreationForm(UserCreationForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "input-image", 
                "hidden": True
            }
        )
    )

    class Meta:
        model = User
        fields = ["avatar", "username", "password1", "password2"]
