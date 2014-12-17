from django.contrib.auth.models import User
from real_fantasy_adventure_app.models import Quest, Avatar, MyQuest
from real_fantasy_adventure_app.forms import AvatarForm, UserForm, MyQuestForm

def inc_professional_points(avatar, hrs_professional):
	"""Increases the avatars num_professional_points by integer placed as 2nd parameter"""
	new_num_professional_points = avatar.num_professional_points + hrs_professional
	avatar.num_professional_points = new_num_professional_points
	avatar.save()

def inc_athletic_points(avatar, hrs_athletic):
	"""Increases the avatars num_athletic_points by integer placed as 2nd parameter"""
	new_num_athletic_points = avatar.num_athletic_points + hrs_athletic
	avatar.num_athletic_points = new_num_athletic_points
	avatar.save()

def inc_academic_points(avatar, hrs_academic):
	"""Increases the avatars num_academic_points by integer placed as 2nd parameter"""	
	new_num_academic_points = avatar.num_academic_points + hrs_academic
	avatar.num_academic_points = new_num_academic_points
	avatar.save()
