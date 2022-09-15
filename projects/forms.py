from django.db import models
from django.forms import ModelForm
from django import forms
from .models import Project


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'