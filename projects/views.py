from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, paginate_projects

def projects(request):
    projects_list, search_query = search_projects(request)

    custom_range, projects_list = paginate_projects(request, projects_list, 3)

    context = {"projects": projects_list, "search_query": search_query, "custom_range": custom_range}

    return render(request, "projects/projects.html", context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        review = review_form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()
        project_obj.get_vote_count
        messages.success(request, 'Your review was successfully submitted!')
        return redirect('single-project', pk=project_obj.id)


    return render(request, "projects/single-project.html", {"project": project_obj, "form": review_form})


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