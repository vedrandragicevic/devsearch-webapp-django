from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import paginateProjects


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    


    context = {
        "projects": projects, 
        'search_query': search_query,
        'custom_range': custom_range
        }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = Tag.objects.all()
    return render(request, 'projects/single-project.html', {'project': project, 'tags': tags})


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':      
        # print(request.POST) -> PRINTS DICT IN TERMINAL
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # RETURNS INSTANCE OF THAT PROJECT
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    # ONLY THE OWNER CAN UPDATE THAT PROJECT
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':      
        # print(request.POST) -> PRINTS DICT IN TERMINAL
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)