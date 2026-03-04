from django import forms
from django.forms import ModelForm

from tasks.models import Task, Worker, Position, TaskType


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees", "team"]


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees", "team"]


class WorkerRegistrationForm(ModelForm):
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput())

    class Meta:
        model = Worker
        fields = [
            "username",
            "email",
            "position",
            "first_name",
            "last_name"
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        else:
            return cleaned_data


class FormWorkerUpdate(ModelForm):
    prev_password = forms.CharField(required=False, max_length=255, widget=forms.PasswordInput())
    new_password = forms.CharField(required=False, max_length=255, widget=forms.PasswordInput())

    class Meta:
        model = Worker
        fields = [
            "username",
            "email",
            "position",
            "first_name",
            "last_name"
        ]

    def clean(self):
        cleaned_data = super().clean()
        worker = self.instance

        if cleaned_data.get("new_password"):
            if not worker.check_password(cleaned_data.get("prev_password")):
                raise forms.ValidationError("Wrong previous password")
            if cleaned_data.get("prev_password") == cleaned_data.get("new_password"):
                raise forms.ValidationError("Please, don't repeat your previous password")
            else:
                return cleaned_data
        else:
            return cleaned_data


class PositionCreateForm(ModelForm):
    class Meta:
        model = Position
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Position.objects.filter(name=name).exists():
            raise forms.ValidationError("Position already exists")
        return name


class TaskTypesCreateForm(ModelForm):
    class Meta:
        model = TaskType
        fields = ["name"]
