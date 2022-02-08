from .models import Profile, Skill
from django.db.models import Q
# Q object encapsulates a SQL expression in a Python object that can be used in database-related operations



def searchProfiles(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    # IMPORT Q AT THE TOP AND WRAP SEARCH QUERIES WITH IT
    profiles = Profile.objects.distinct().filter(Q(name__icontains = search_query) | Q(short_intro__icontains = search_query) | Q(skill__in=skills))
    return profiles, search_query