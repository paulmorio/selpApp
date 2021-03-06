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

	def clean_nickname(self):
	    data = self.cleaned_data['nickname']
	    if Avatar.objects.filter(nickname=data).exists():
	        raise forms.ValidationError("This nickname is already being used")
	    return data

class MyQuestForm(forms.ModelForm):
	"""docstring for MyQuestForm"""
	title = forms.CharField(max_length=256, help_text="Give a title for your MyQuest")
	description = forms.CharField(widget=forms.Textarea, help_text="Describe your MyQuest, its only visible by you so dont worry about spelling :)")

	req_professional_points = forms.IntegerField(initial=0, label="Required Professional Points")
	req_athletic_points = forms.IntegerField(initial=0, label="Required Athletic Points")
	req_academic_points = forms.IntegerField(initial=0, label="Required Academic Points")

	slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = MyQuest
		fields = ('title', 'description', 'req_professional_points', 'req_athletic_points', 'req_academic_points')
		exclude = ('avatar',)

class StatChangeForm(forms.ModelForm):
	"""docstring for StatChangeForm"""
	num_professional_points = forms.IntegerField(initial=0, help_text="How many hours did you work professionally today", label="Professional")
	num_athletic_points = forms.IntegerField(initial=0, help_text="How many hours did you spend exercising today?", label="Athletic")
	num_academic_points = forms.IntegerField(initial=0, help_text="How many hours did you spend studying today?", label="Academic")

	class Meta:
		model = Avatar
		fields = ('num_professional_points','num_athletic_points', 'num_academic_points')
		exclude = ('avatar',)
