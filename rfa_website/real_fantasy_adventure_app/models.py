from django.db import models
from django.utils import timezone

#####################################
######         AVATARS         ######
#####################################
class AvatarQuerySet(models.QuerySet):
	def confirmed(self):
		return self.filter(confirm=True)

# Avatar Model
class Avatar(models.Model):
	"""docstring for Avatar"""
	# General
	name = models.CharField(max_length=200)
	bio = models.TextField()
	confirm = models.BooleanField(default=False)

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

	# For more helpful errors
	def __str__(self):
		return self.name
	def __unicode__(self):
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

	# Minimum Required Points to Vieq Quests
	min_num_professional_points = models.IntegerField(default=1)
	min_num_athletic_points = models.IntegerField(default=1)
	min_num_academic_points = models.IntegerField(default=1)

	# Rewarding Points
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

	# For more helpful errors.
	def __str__(self):
		return self.title
	def __unicode__(self):
		return self.title
	
	class Meta:
		verbose_name = "Quest Entry"
		verbose_name_plural = "Quest Entries"
		ordering = ["-created_date"]


#####################################
######        MyQuests         ######
#####################################
# MyQuest Query Set
class MyQuestQuerySet(models.QuerySet):
	def published(self):
		return self.filter(publish=True)

# MyQuest Model
class MyQuest(models.Model):
	"""MyQuest are Quests written by avatars for themselves to achieve, however
	 they are not subclasses as they should not include some fields Quests has"""
	avatar = models.ForeignKey(Avatar)
	title = models.CharField(max_length=256)
	description = models.TextField()
	publish = models.BooleanField(default=False)

	# Requirements for clearing
	req_professional_points = models.IntegerField(default=1)
	req_athletic_points = models.IntegerField(default=1)
	req_academic_points = models.IntegerField(default=1)

	# Reward Points (how to model this?)

	# URL Friendly Reference
	slug = models.SlugField(max_length=200, unique=True)

	#Date Attributes
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	# Connection to Queryset for admin tasks
	objects = MyQuestQuerySet.as_manager()	

	#For helpful errors
	def __str__(self):
		return self.title
	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = "MyQuest Entry"
		verbose_name_plural = "MyQuest Entries"
		ordering = ["-created_date"]

