from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

def projects(request):
    projectsList = Project.objects.all()
    context = {"projects": projectsList}

    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()

    return render(request, "projects/single-project.html", {"project": projectObj})


@login_required(login_url="login")
def create_project(request):
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def update_project(request, pk):
    existing_project = Project.objects.get(id=pk)
    form = ProjectForm(instance=existing_project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=existing_project)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    context = {"object": project}

    if request.method == "POST":
        project.delete()
        return redirect("projects")
    
    return render(request, 'projects/delete_template.html', context)