from django.shortcuts import render
from django.http import HttpResponse
from .models import Project

projectsList = [
    {
        "id": "1",
        "title": "Ecommerce Website",
        "description": "Fully functional e-commerce website",
    },
    {
        "id": "2",
        "title": "Portfolio Website",
        "description": "This was a project where I built my portfolio",
    },
    {
        "id": "3",
        "title": "Social Network",
        "description": "Awesome open-source project I am still working on",
    },
]


def projects(request):
    projectsList = Project.objects.all()
    context = {"projects": projectsList}

    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()

    return render(
        request, "projects/single-project.html", {"project": projectObj}
    )
