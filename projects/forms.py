from django.forms import ModelForm, widgets
from django import forms
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        # CREATES A FORM BASED ON CLASS PROJECT FROM models.py
        model = Project
        fields = ['title', 'featured_image','description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.base_fields.items():
                
            field.widget.attrs.update({'class':'input'})