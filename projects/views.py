from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm


def projects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = Tag.objects.all()
    return render(request, 'projects/single-project.html', {'project': project, 'tags': tags})


def createProject(request):
    form = ProjectForm()
    context = {'form': form}
    return render(request, "projects/project_form.html", context)