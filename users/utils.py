from .models import Profile, Skill
from django.db.models import Q
# Q object encapsulates a SQL expression in a Python object that can be used in database-related operations
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):
    # Pagination implementation with custom range
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    # Solving the problem that occurs if we have for example 100 buttons on a single page
    leftIndex = (int(page)-4)

    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles



def searchProfiles(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    # IMPORT Q AT THE TOP AND WRAP SEARCH QUERIES WITH IT
    profiles = Profile.objects.distinct().filter(Q(name__icontains = search_query) | Q(short_intro__icontains = search_query) | Q(skill__in=skills))
    return profiles, search_query