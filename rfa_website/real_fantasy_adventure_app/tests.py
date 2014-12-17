from django.test import TestCase
from django.contrib.auth import get_user_model
from . models import Quest, Avatar, MyQuest
from django.contrib.auth.models import User
from . statChange import inc_professional_points, inc_athletic_points, inc_academic_points

# TestCases for Quest Models
class QuestEntryTest(TestCase):

	def test_create_unpublished(self):
		"""
		Creates a Quest instance that is unconfirmed, makes sure the 
		queryset doesnt find this, confirms the instance, and tries 
		the search again
		"""
		quest = Quest(title="Test Title", description="Test Description", publish=False)
		quest.save()
		self.assertEqual(Quest.objects.all().count(), 1)
		self.assertEqual(Quest.objects.published().count(), 0)
		quest.publish = True
		quest.save()
		self.assertEqual(Quest.objects.published().count(), 1)

# TestCases for Avatar Models
class AvatarEntryTest(TestCase):

	def test_create_unconfirmed(self):
		"""
		Creates a Avatar instance that is unconfirmed, makes sure the 
		queryset doesnt find this, confirms the instance, and tries the search again
		"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		avatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=False)
		avatar.save()
		self.assertEqual(Avatar.objects.all().count(), 1)
		self.assertEqual(Avatar.objects.confirmed().count(), 0)
		avatar.confirm = True
		avatar.save()
		self.assertEqual(Avatar.objects.confirmed().count(), 1)

	def test_slug_line_creation(self):
		"""
		tests the proper creation of slugs depending on the nickname of the avatar 
		(ie. Random String --> random-string)
		"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		avatar = Avatar(user=testUser, nickname="Random String", bio="Test Biography", confirm=False)
		avatar.save()
		self.assertEqual(avatar.slug, 'random-string')

# TestCases for MyQuest Models
class MyQuestEntryTest(TestCase):
	
	def test_create_unpublished(self):
		"""
		Creates a MyQuest instance that is unconfirmed, makes sure the 
		queryset doesnt find this, confirms the instance, and tries 
		the search again
		"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()
		myQuest = MyQuest(avatar=testAvatar, title="TestTitle", description="Test Description", publish=False)
		myQuest.save()
		self.assertEqual(MyQuest.objects.all().count(), 1)
		self.assertEqual(MyQuest.objects.published().count(), 0)
		myQuest.publish = True
		myQuest.save()
		self.assertEqual(MyQuest.objects.published().count(), 1)

	def test_slug_line_creation(self):
		"""
		tests the proper creation of slugs depending on the title of the myQuest 
		(ie. Random String --> random-string)
		"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()
		myQuest = MyQuest(avatar=testAvatar, title="Random String", description="Test Description", publish=False)
		myQuest.save()
		self.assertEqual(myQuest.slug, 'random-string')

