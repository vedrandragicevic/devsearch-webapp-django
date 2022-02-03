from pydoc import describe
from django.shortcuts import render
from .models import Profile

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # IF THE SKILL DOESN'T HAVE A DESCRIPTION, FILTER IT OUT
    # EXCLUDE EVERYTHING THAT MATCHES description_exact=""
    topSkills = profile.skill_set.exclude(description="")
    # GIVE ME ALL THE VALUES THAT CONTAIN description=""
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile,
    'topSkills': topSkills,
    'otherSkills': otherSkills
    }
    return render(request, 'users/user-profile.html', context)