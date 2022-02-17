from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import Project, ProjectSerializer
from projects.models import Project, Tag, Review
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    # Get user from token
    user = request.user.profile
    data = request.data

    """
    get_or_create(defaults=None, **kwargs)
        A convenience method for looking up an object with the given kwargs (may be empty if your model has defaults for all fields), creating one if necessary.
        Returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.
        This is meant to prevent duplicate objects from being created when requests are made in parallel, and as a shortcut to boilerplatish code
    """
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project 
    )
    review.value = data['value']
    review.save()
    project.getVoteCount

    # many = False to get only one project
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)