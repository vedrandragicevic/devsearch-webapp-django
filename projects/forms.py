import imp
from django.forms import ModelForm
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        # CREATES A FORM BASED ON CLASS PROJECT FROM models.py
        model = Project
        fields = '__all__'