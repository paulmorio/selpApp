from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

#####################################
######         AVATARS         ######
#####################################
class AvatarQuerySet(models.QuerySet):
	def confirmed(self):
		return self.filter(confirm=True)

# Avatar Model
class Avatar(models.Model):
	"""
	The Avatar is the basic model of the rfa-application. It is the user's
	connection to the application and User instances share a one to one 
	relationship with avatar instances.

	It is important to note that a different save than django standard save
	function has been implemented in order to save the slug field correctly.
	"""
	# Links Avatar to User Model instnace
	user = models.OneToOneField(User)
	
	# Avatar fields from here
	nickname = models.CharField(max_length=80)
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
	slug = models.SlugField(max_length=80, unique=True)

	# Connection to its queryset for admin tasks
	objects = AvatarQuerySet.as_manager()

	# new save function
	def save(self, *args, **bargs):
		self.slug = slugify(self.nickname)
		super(Avatar, self).save(*args, **bargs)

	# For more helpful errors
	def __str__(self):
		return self.user.username
	def __unicode__(self):
		return self.user.username

	def get_total_points(self):
		return self.num_professional_points + self.num_athletic_points + self.num_academic_points

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
	"""
	Quests are a currently planned functional entity in the rfa-application they are different
	from MyQuests in that they have additional fields and should only be created by staff level
	people of the application.

	The fundamental difference is that they can actually reward players by increasing the
	number of points of avatars if they are cleared.

	However difficulty in understanding how to handle the clearing (and not being able to 
	clear it again) has made this an unimplemented feature.
	"""
	title = models.CharField(max_length=256)
	description = models.TextField()
	publish = models.BooleanField(default=False)

	# Minimum Required Points to View Quests
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
	"""
	MyQuest are Quests written by avatars for themselves to achieve, however
	they are not subclasses as they should not include some fields Quests has
	and have a fundamentally different role from them.

	MyQuests share a many to one relationship to avatars. ie. one avatar has
	many MyQuests.
	"""
	avatar = models.ForeignKey(Avatar)
	title = models.CharField(max_length=256)
	description = models.TextField()
	publish = models.BooleanField(default=False)

	# Requirements for clearing
	req_professional_points = models.IntegerField(default=1)
	req_athletic_points = models.IntegerField(default=1)
	req_academic_points = models.IntegerField(default=1)

	# URL Friendly Reference
	slug = models.SlugField(max_length=200, unique=True)

	#Date Attributes
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	# Connection to Queryset for admin tasks
	objects = MyQuestQuerySet.as_manager()

	# new save function
	def save(self, *args, **bargs):
		self.slug = slugify(self.title)
		super(MyQuest, self).save(*args, **bargs)

	#For helpful errors
	def __str__(self):
		return self.title
	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = "MyQuest Entry"
		verbose_name_plural = "MyQuest Entries"
		ordering = ["-created_date"]

