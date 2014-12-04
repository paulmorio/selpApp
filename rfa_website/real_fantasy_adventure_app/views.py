from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from . import models
# Create your views here.

# class QuestIndex(generic.ListView):
# 	queryset = models.Entry.objects.published()
# 	template = "quests.html"
# 	paginate_by = 5

def index(request):
	return HttpResponse("Welcome Hero, this is just a test site, your princess is in another castle")

