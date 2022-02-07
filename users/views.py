from pydoc import describe
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, profileForm


def loginUser(request):
    page = 'register'
    
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'USERNAME DOES NOT EXIST')

        # QUERYING THE DATABASE
        user = authenticate(request, username=username, password=password)

        # login FUNCTION CREATES SESSION FOR THE USER
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "USERNAME OR PASSWORD IS INCORRECT")

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'USER WAS LOGGED OUT')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # HOLDING THE USER BEFORE PROCESSING IT, FOR MODIFICATION
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(request, 'An error has occurred during registration!')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


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


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    # PASS instance TO PRE FILL DATA
    form = profileForm(instance=profile)

    if request.method == 'POST':
        form = profileForm(request.POST, request.FILE, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)