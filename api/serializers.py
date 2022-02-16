from rest_framework import serializers
from projects.models import Project


# Takes Project model and converts it into a json object
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'