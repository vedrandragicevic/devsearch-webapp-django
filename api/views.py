from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import Project, ProjectSerializer
from projects.models import Project, Tag
from users.models import Profile


@api_view(['GET'])
def getRoutes(request):
    """
        Shows all available routes in the app.
    """
    routes = [
        {
            'GET': '/api/projects'
            },
        {
            'GET': '/api/projects/id'
            },
        {
            'POST': '/api/projects/id/vote'
            },
        {
            'POST': '/api/users/token'
            },
        {
            'POST': '/api/users/token/refresh'
            }
    ]

    return Response(routes)


# Permission classes decorator limits user to see projects only if he's authenticated
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    # Takes query set and transforms it into JSON
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    # Takes query set and transforms it into JSON
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)