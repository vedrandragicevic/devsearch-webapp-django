from django.forms import ModelForm, widgets
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        # CREATES A FORM BASED ON CLASS PROJECT FROM models.py
        model = Project
        fields = ['title', 'featured_image','description', 'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'input'})
        self.fields['featured_image'].widget.attrs.update({'class':'input'})
        self.fields['description'].widget.attrs.update({'class':'input'})
        self.fields['demo_link'].widget.attrs.update({'class':'input'})
        self.fields['source_link'].widget.attrs.update({'class':'input'})

    
class ReviewForm(ModelForm):
    class Meta:
        # CREATES A FORM BASED ON CLASS REVIEW FROM models.py
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['value'].widget.attrs.update({'class':'input'})
        self.fields['body'].widget.attrs.update({'class':'input'})
       