from django.db import models
from django.utils import timezone

# Create your models here.

# Avatar model
class Avatar(models.Model):
	"""The Avatar is the User's character within the game"""
	username = models.ForeignKey("auth.User")
	level = models.IntegerField(default=1)
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.username
		
# # Quest model
# class Quest(models.Model):
# 	"""docstring for Quest"""
# 	title = models.CharField(max_length=256)
# 	description = models.TextField()
# 	created_date = models.DateTimeField(default=timezone.now)
# 	min_Avatar_Level_Requirement = models.IntegerField(default=1)
# 	rewardPoints = 


# 	def __init__(self, arg):
# 		super(Quest, self).__init__()
# 		self.arg = arg

# 	def __str__(self):
# 		return self.title
		


# # Points Model
# class Point(models.Model):
# 	"""docstring for Point"""
# 	def __init__(self, arg):
# 		super(Point, self).__init__()
# 		self.arg = arg
