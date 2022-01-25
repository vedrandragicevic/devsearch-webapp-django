from django.shortcuts import render
from django.http import HttpResponse

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
    page = "projects"
    number = 10
    context = {"page": page, "number": number, "projects": projectList}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = None
    for i in projectList:
        if i["id"] == pk:
            projectObj = i
    return render(request, 'projects/single-project.html', {'project': projectObj})
