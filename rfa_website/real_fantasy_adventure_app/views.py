from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from real_fantasy_adventure_app.models import Quest, Avatar, MyQuest

# Create your views here.

# class QuestIndex(generic.ListView):
# 	queryset = models.Entry.objects.published()
# 	template = "quests.html"
# 	paginate_by = 5

# Old index view handler
# def index(request):
# 	return HttpResponse("Welcome Hero, this is just a test site, your princess is in another castle")

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


