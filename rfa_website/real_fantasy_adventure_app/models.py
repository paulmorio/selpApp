from django.db import models
from django.utils import timezone

#Avatar model
# class Avatar(models.Model):
# 	"""The Avatar is the User's character/profile within the game"""
# 	realUser = models.ForeignKey(User)

# 	biography = models.TextField(blank=True)
# 	level = models.IntegerField(default=1)
# 	created_date = models.DateTimeField(dauto_now_add=True)
# 	modified_date = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return __str__(realUser)
#####################################
######         AVATARS         ######
#####################################
class AvatarQuerySet(models.QuerySet):
	def confirmed(self):
		return self.filter(confirm=True)

# Avatar Model
class Avatar(object):
	"""docstring for Avatar"""
	# General
	name = models.CharField(max_length=200)
	bio = models.TextField()

	# Level (important to access Quests)
	level = models.IntegerField(default=1)

	# Point Categories
	num_professional_points = models.IntegerField(default=0)
	num_athletic_points = models.IntegerField(default=0)
	num_academic_points = models.IntegerField(default=0)

	# Date Related Attributes
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	# URL Friendly Reference (for use with profile pages)
	slug = models.SlugField(max_length=200, unique=True)

	# Connection to its queryset for admin tasks
	objects = AvatarQuerySet.as_manager()

	def __str__(self):
		return self.name

	def get_total_points():
		return num_professional_points + num_academic_points + num_athletic_points

	class Meta:
		verbose_name = "Avatar Entry"
		verbose_name_plural = "Avatar Entries"
		ordering = ["-level"]

#####################################
######         QUESTS          ######
#####################################
class QuestQuerySet(models.QuerySet):
	def published(self):
		return self.filter(publish=True)

# Quest model
class Quest(models.Model):
	"""docstring for Quest"""
	title = models.CharField(max_length=256)
	description = models.TextField()
	publish = models.BooleanField(default=False)

	# Point Categories
	num_professional_points = models.IntegerField(default=0)
	num_athletic_points = models.IntegerField(default=0)
	num_academic_points = models.IntegerField(default=0)

	# URL Friendly Reference
	slug = models.SlugField(max_length=200, unique=True)

	#Date Attributes
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	# Connection to Queryset for admin tasks
	objects = QuestQuerySet.as_manager()

	# ONCE AVATAR HAS BEEN Makde
	#min_Avatar_Level_Requirement = models.IntegerField(default=1)
	#rewardPoints = 

	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = "Quest Entry"
		verbose_name_plural = "Quest Entries"
		ordering = ["-created_date"]
