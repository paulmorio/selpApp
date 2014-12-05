from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views import generic
from django.template import RequestContext
from . import models
# Create your views here.

# class QuestIndex(generic.ListView):
# 	queryset = models.Entry.objects.published()
# 	template = "quests.html"
# 	paginate_by = 5

# Old index view handler
# def index(request):
# 	return HttpResponse("Welcome Hero, this is just a test site, your princess is in another castle")

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('real_fantasy_adventure_app/index.html', context_dict, context)

def about(request):
	context = RequestContext(request)
	context_dict = {'boldthing' : "You are an adventurer"}

	return render_to_response('real_fantasy_adventure_app/about.html', context_dict, context)