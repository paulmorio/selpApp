from django import forms
from real_fantasy_adventure_app.models import Avatar, Quest, MyQuest

class AvatarForm(forms.ModelForm):
	"""docstring for AvatarForm"""
	name = forms.CharField(max_length=200, help_text="Please Enter a UserName for the Avatar")
	bio = forms.TextField(help_text="Write a little about yourself or your avatar")

	slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Avatar
				fields = ('name',)


class QuestForm(forms.ModelForm):
	"""docstring for QuestForm"""
	title = forms.CharField(max_length=256, help_text="Please Enter A Title for this Quest")
	description = forms.TextField(help_text="Please enter more detailed description of the quest, be creative!")

	slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

	# Minimum number of points required to view quest
	min_num_professional_points = forms.IntegerField(default=1)
	min_num_athletic_points = forms.IntegerField(default=1)
	min_num_academic_points = forms.IntegerField(default=1)

	# Rewarding Points
	reward_num_professional_points = forms.IntegerField(default=0)
	reward_num_athletic_points = forms.IntegerField(default=0)
	reward_num_academic_points = forms.IntegerField(default=0)

	class Meta:
		model = Quest
				fields = ('title',)

class MyQuestForm(forms.ModelForm):
	"""docstring for MyQuestForm"""
	title = forms.CharField(max_length=256, help_text="Please Enter a title for your Quest")
	description = forms.TextField()

	# Requirements for clearing
	req_professional_points = forms.IntegerField(default=1)
	req_athletic_points = forms.IntegerField(default=1)
	req_academic_points = forms.IntegerField(default=1)


	class Meta:
		model = MyQuest
				exclude = ('avatar',)
				fields = ('title',)
