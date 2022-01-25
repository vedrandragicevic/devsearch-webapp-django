from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, Tag

projectList = [
    {
        "id": 1,
        "title": "Ecommerce website",
        "description": "Fully functional ecommerce website"
    },
    {
        "id": 2,
        "title": "Portfolio website",
        "description": "This was a project where I build my portfolio"
    },
    {
        "id": 3,
        "title": "Social Network",
        "description": "Awesome open source project I'm still working on"
    }
]


def projects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = Tag.objects.all()
    return render(request, 'projects/single-project.html', {'project': project, 'tags': tags})
