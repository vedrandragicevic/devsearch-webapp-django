import imp
from multiprocessing import context
from pydoc import describe
from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, profileForm, SkillForm, MessageForm
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles


def loginUser(request):
    page = 'register'
    
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
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
            # TODO - FIX THIS REDIRECT
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
    # CALLING FUNCTION FROM UTILS.PY
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # IF THE SKILL DOESN'T HAVE A DESCRIPTION, FILTER IT OUT
    # EXCLUDE EVERYTHING THAT MATCHES description_exact=""
    topSkills = profile.skill_set.exclude(description="")
    # GIVE ME ALL THE VALUES THAT CONTAIN description=""
    otherSkills = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills
    }
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    """
        Suppose you have a model Car and a model Wheel. Wheel has a foreign key relationship with Car as follows:
            class Car(models.Model):
                pass

            class Wheel(models.Model):
                car = models.ForeignKey(Car, on_delete=models.CASCADE)

        Let's say w is an instance of Wheel, and c is an instance of Car:
            w.car # returns the related Car object to w
            c.wheel_set.all() # returns all Wheel objects related to c
    """
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


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was created!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated!')
            return redirect('account')
            
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    # messages is related name in the model
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read=False).count()

    context = {'messageRequest': messageRequest, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    # When a user opens the message, change to read 
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recepient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recepient = recepient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            # When you send somebody a message, you'll be redirected to their account
            return redirect('user-profile', pk=recepient.id)
    
    context = {'recepient': recepient, 'form': form}
    return render(request, 'users/message_form.html', context)


