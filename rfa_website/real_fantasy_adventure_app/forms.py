from django import forms
from django.contrib.auth.models import User
from real_fantasy_adventure_app.models import Avatar, Quest, MyQuest

class UserForm(forms.ModelForm):
	"""docstring for UserForm"""
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class AvatarForm(forms.ModelForm):
	"""docstring for AvatarForm"""
	nickname = forms.CharField(max_length=80, help_text="Give yourself a nickname, if you cant think of one, this can just be your username")
	bio = forms.CharField(widget=forms.Textarea, help_text="Write a little about yourself or your avatar")

	slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Avatar
		fields = ('nickname', 'bio')

class MyQuestForm(forms.ModelForm):
	"""docstring for MyQuestForm"""
	title = forms.CharField(max_length=256, help_text="Give a title for your MyQuest")
	description = forms.CharField(widget=forms.Textarea, help_text="Describe your MyQuest, its only visible by you so dont worry about spelling :)")

	req_professional_points = forms.IntegerField(initial=0)
	req_athletic_points = forms.IntegerField(initial=0)
	req_academic_points = forms.IntegerField(initial=0)

	slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = MyQuest
		fields = ('title', 'description', 'req_professional_points', 'req_athletic_points', 'req_academic_points')
		exclude = ('avatar',)


# class QuestForm(forms.ModelForm):
# 	"""docstring for QuestForm"""
# 	title = forms.CharField(max_length=256, help_text="Please Enter A Title for this Quest")
# 	description = forms.TextField(help_text="Please enter more detailed description of the quest, be creative!")

# 	slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

# 	# Minimum number of points required to view quest
# 	min_num_professional_points = forms.IntegerField(default=1)
# 	min_num_athletic_points = forms.IntegerField(default=1)
# 	min_num_academic_points = forms.IntegerField(default=1)

# 	# Rewarding Points
# 	reward_num_professional_points = forms.IntegerField(default=0)
# 	reward_num_athletic_points = forms.IntegerField(default=0)
# 	reward_num_academic_points = forms.IntegerField(default=0)

# 	class Meta:
# 		model = Quest
# 				fields = ('title',)

# class MyQuestForm(forms.ModelForm):
# 	"""docstring for MyQuestForm"""
# 	title = forms.CharField(max_length=256, help_text="Please Enter a title for your Quest")
# 	description = forms.TextField()

# 	# Requirements for clearing
# 	req_professional_points = forms.IntegerField(default=1)
# 	req_athletic_points = forms.IntegerField(default=1)
# 	req_academic_points = forms.IntegerField(default=1)


# 	class Meta:
# 		model = MyQuest
# 				exclude = ('avatar',)
# 				fields = ('title',)
