from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from .utils import search_projects

def projects(request):
    projects_list, search_query = search_projects(request)

    context = {"projects": projects_list, "search_query": search_query}

    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()

    return render(request, "projects/single-project.html", {"project": projectObj})


@login_required(login_url="login")
def create_project(request):
    user_profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = user_profile
            project.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def update_project(request, pk):
    user_profile = request.user.profile
    existing_project = user_profile.project_set.get(id=pk)
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
    user_profile = request.user.profile
    project_to_delete = user_profile.project_set.get(id=pk)
    context = {"object": project}

    if request.method == "POST":
        project_to_delete.delete()
        return redirect("projects")
    
    return render(request, 'delete_template.html', context)