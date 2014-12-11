from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from real_fantasy_adventure_app.models import Quest, Avatar, MyQuest

# Create your views here.

def index(request):

    # make a list of the top 5 players by points
    avatars_by_academic = Avatar.objects.order_by('-num_academic_points')[:5]
    avatars_by_professional = Avatar.objects.order_by('-num_professional_points')[:5]
    avatars_by_athletic = Avatar.objects.order_by('-num_athletic_points')[:5]

    # make a context dictionary for each
    context_dict = {'academics': avatars_by_academic, 'professionals': avatars_by_professional, 'athletes': avatars_by_athletic}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'real_fantasy_adventure_app/index.html', context_dict)

def about(request):
	context_dict = {'boldthing' : "You are an adventurer"}

	return render(request, 'real_fantasy_adventure_app/about.html', context_dict)

def avatarProfile(request, avatar_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a avatar name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        avatar = Avatar.objects.get(slug=avatar_name_slug) 

        context_dict['avatar_name'] = avatar.name

        # Retrieve all of the associated myQuests.
        # Note that filter returns >= 1 model instance.
        myQuests = MyQuest.objects.filter(avatar=avatar)

        # Adds our results list to the template context under name myQuests.
        context_dict['myQuests'] = myQuests
        # We also add the avatar object from the database to the context dictionary.
        # We'll use this in the template to verify that the avatar exists.
        context_dict['avatar'] = avatar

    except Avatar.DoesNotExist:
        # We get here if we didn't find the specified avatar.
        # Don't do anything - the template displays the "no avatar" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'real_fantasy_adventure_app/avatarProfile.html', context_dict)