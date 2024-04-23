from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import *
from projects.models import *

# Common practice to create a getRoutes function to display all available routes for information purposes.
@api_view(["GET"])
def get_routes(request):

    routes = [
        {"GET": "/api/projects"},
        {"GET": "/api/projects/id"},
        {"POST": "/api/projects/id/vote"},
        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]

    return Response(routes, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_projects(request):
    projects = Project.objects.all()
    # Many property is set to True because we are serializing multiple objects.
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_single_project(request, uuid):
    project = Project.objects.get(id=uuid)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def project_vote(request, uuid):
    project = Project.objects.get(id=uuid)
    user = request.user.profile
    data = request.data

    # This prevents duplicate records from being created for the same user and project.
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    review.value = data["value"]
    review.save()
    project.get_vote_count

    # Return the project to see the most recent vote count.
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)