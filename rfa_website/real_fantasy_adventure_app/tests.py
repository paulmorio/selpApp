from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from . models import Quest, Avatar, MyQuest
from django.contrib.auth.models import User
from . statChange import inc_professional_points, inc_athletic_points, inc_academic_points
from django.core.urlresolvers import reverse


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

	def test_get_total_points(self):
		"""
		Tests the get_total_points() function for correctness
		"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		avatar = Avatar(user=testUser, nickname="Random String", bio="Test Biography", confirm=False, num_professional_points=1, num_athletic_points=2, num_academic_points=3)
		avatar.save()
		self.assertEqual(avatar.get_total_points(), 6)	

# TestCases for MyQuest Models
class MyQuestEntryTest(TestCase):
	"""
	Tests Section of the MyQuest model, each test function's docstring explains 
	what is tested better
	"""
	
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

	def test_belong_to_only_one_avatar(self):
		"""
		Asserts that myQuests only belong to one avatar.
		"""
		testUser1 = User.objects.create_user(username = "testUser1", email="test1@test.com", password="test1234")
		testAvatar1 = Avatar(user=testUser1, nickname="TestName1", bio="Test1 Biography", confirm=True)
		testAvatar1.save()
		myQuest1 = MyQuest(avatar=testAvatar1, title="Random String1", description="Test Description", publish=False)
		myQuest1.save()

		testUser2 = User.objects.create_user(username = "testUser2", email="test2@test.com", password="test1234")
		testAvatar2 = Avatar(user=testUser2, nickname="TestName2", bio="Test Biography", confirm=True)
		testAvatar2.save()
		myQuest2 = MyQuest(avatar=testAvatar2, title="Random String2", description="Test Description", publish=False)
		myQuest2.save()

		testUser3 = User.objects.create_user(username = "testUser3", email="test3@test.com", password="test1234")
		testAvatar3 = Avatar(user=testUser3, nickname="TestName3", bio="Test Biography", confirm=True)
		testAvatar3.save()
		myQuest3 = MyQuest(avatar=testAvatar2, title="Random String3", description="Test Description", publish=False)
		myQuest3.save()

		self.assertEqual(MyQuest.objects.filter(avatar=testAvatar2).count(), 2)
		self.assertEqual(MyQuest.objects.filter(avatar=testAvatar1).count(), 1)
		self.assertEqual(MyQuest.objects.filter(avatar=testAvatar3).count(), 0)

class UserEntryTests(TestCase):
	"""
	Tests concerning users, as this module part of the django package, only minimal testing of
	functions of interest are tested once again.
	"""

	def test_set_up_users_a_and_b(self):
		a = User.objects.create_user(username="a", email="test@test.com", password="test1234")
		b = User.objects.create_user(username="b", email="test@test.com", password="test1234")
		c = User.objects.get(username="a")
		d = User.objects.get(username="b")
		self.assertEqual(a,c)
		self.assertEqual(b,d)
		self.assertNotEqual(a,d)

	def test_check_usernames(self):
		a = User.objects.create(username="a")
		b = User.objects.create(username="b")
		self.assertEqual(a.username, "a")
		self.assertEqual(b.username, "b")
		

class IndexViewTests(TestCase):
	"""
	Class contains tests for the index view, the docstrings of each test function 
	explain what is tested
	"""

	def test_index_view_with_no_academics(self):
		"""If no avatars exist, the appopiate message is displayed."""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "There are no academics present.")
		self.assertQuerysetEqual(response.context['academics'], [])

	def test_index_view_with_no_professsionals(self):
		"""If no avatars exist, the appropiate message is displayed"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "There are no professionals present.")
		self.assertQuerysetEqual(response.context['professionals'], [])

	def test_index_view_with_no_athletes(self):
		"""If no avatars exist, the appropiate message is displayed"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "There are no athletes present.")
		self.assertQuerysetEqual(response.context['athletes'], [])

	def test_index_view_with_academics(self):
		"""If avatars exist, the appopiate content is displayed."""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertNotContains(response, "There are no academics present.")

		num_avatars = len(response.context['academics'])
		self.assertEqual(num_avatars, 1)

	def test_index_view_with_professsionals(self):
		"""If avatars exist, the appropiate content is displayed"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertNotContains(response, "There are no professionals present.")

		num_avatars = len(response.context['professionals'])
		self.assertEqual(num_avatars, 1)

	def test_index_view_with_athletes(self):
		"""If avatars exist, the appropiate content is displayed"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertNotContains(response, "There are no athletes present.")

		num_avatars = len(response.context['athletes'])
		self.assertEqual(num_avatars, 1)

	def test_index_view_without_authentication_own_avatar_link(self):
		"""
		If the user is not logged in, then there should be no link 
		that goes to the avatar profile but a <p> item that tells
		the visitor that a link will appear once he/she logs in.
		"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "If you log-in, a link will appear here that links you straight to your avatar")

	def test_index_view_without_authentication_register_link(self):
		"""If the user is not logged in, there should be a register link"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Register")

	def test_index_view_without_authentication_about_link(self):
		"""If the user is not logged in, there should be a about link"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "About")

	def test_index_view_without_authentication_log_in_link(self):
		"""If the user is not logged in, there should be a log-in link"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Log-In")

	def test_index_view_without_authentication_appropiate_header(self):
		"""If the user is not logged in, there should be a appropiate message in the header"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Hello adventurer you are not logged in!")

	def test_index_view_authenticated_youravatar_link(self):
		"""Checks if the your avatar link is available if logged in user present"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		# log in this user
		self.client.login(username="testUser", password="test1234")

		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Your Avatar Page")

	def test_index_view_authenticated_logout(self):
		"""Checks if the logout link is available if logged in user present"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		# log in this user
		self.client.login(username="testUser", password="test1234")

		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Logout")

	def test_index_view_authenticated_appropiate_header(self):
		"""Checks if the appropiate header is available if logged in"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		# log in this user
		self.client.login(username="testUser", password="test1234")

		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertNotContains(response, "Hello adventurer you are not logged in!")


class RankingsViewTests(TestCase):
	"""
	Class contains tests for the Rankings view, the docstrings of each test function 
	explain what is tested
	"""

	def test_rankings_view_with_no_academics(self):
		"""If no avatars exist, the appopiate message is displayed."""
		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "There are no academics present.")
		self.assertQuerysetEqual(response.context['academics'], [])

	def test_rankings_view_with_no_professsionals(self):
		"""If no avatars exist, the appropiate message is displayed"""
		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "There are no professionals present.")
		self.assertQuerysetEqual(response.context['professionals'], [])

	def test_rankings_view_with_no_athletes(self):
		"""If no avatars exist, the appropiate message is displayed"""
		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "There are no athletes present.")
		self.assertQuerysetEqual(response.context['athletes'], [])

	def test_rankings_view_with_academics(self):
		"""If avatars exist, the appopiate content is displayed."""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertNotContains(response, "There are no academics present.")

		num_avatars = len(response.context['academics'])
		self.assertEqual(num_avatars, 1)

	def test_rankings_view_with_professsionals(self):
		"""If avatars exist, the appropiate content is displayed"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertNotContains(response, "There are no professionals present.")

		num_avatars = len(response.context['professionals'])
		self.assertEqual(num_avatars, 1)

	def test_rankings_view_with_athletes(self):
		"""If avatars exist, the appropiate content is displayed"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertNotContains(response, "There are no athletes present.")

		num_avatars = len(response.context['athletes'])
		self.assertEqual(num_avatars, 1)

	def test_rankings_view_without_authentication_register_link(self):
		"""If the user is not logged in, there should be a register link"""
		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Register")

	def test_rankings_view_without_authentication_about_link(self):
		"""If the user is not logged in, there should be a about link"""
		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "About")

	def test_rankings_view_without_authentication_log_in_link(self):
		"""If the user is not logged in, there should be a log-in link"""
		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Log-In")

	def test_rankings_view_without_authentication_appropiate_header(self):
		"""If the user is not logged in, there should be a appropiate message in the header"""
		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Hello adventurer you are not logged in!")

	def test_rankings_view_authenticated_appropiate_header(self):
		"""Checks if the appropiate header is available if logged in"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		# log in this user
		self.client.login(username="testUser", password="test1234")

		response = self.client.get(reverse('rankings'))
		self.assertEqual(response.status_code,200)
		self.assertNotContains(response, "Hello adventurer you are not logged in!")

class AboutViewTests(TestCase):
	"""
	Class contains tests for the about view, the docstrings of each test function 
	explain what is tested
	"""

	def test_about_view_without_authentication_register_link(self):
		"""If the user is not logged in, there should be a register link"""
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Register")

	def test_about_view_without_authentication_about_link(self):
		"""If the user is not logged in, there should be a about link"""
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "About")

	def test_about_view_without_authentication_log_in_link(self):
		"""If the user is not logged in, there should be a log-in link"""
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Log-In")

	def test_about_view_without_authentication_appropiate_header(self):
		"""If the user is not logged in, there should be a appropiate message in the header"""
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Hello adventurer you are not logged in!")

	def test_about_view_authenticated_appropiate_header(self):
		"""Checks if the appropiate header is available if logged in"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		# log in this user
		self.client.login(username="testUser", password="test1234")

		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code,200)
		self.assertNotContains(response, "Hello adventurer you are not logged in!")

class NotLoggedInViewTests(TestCase):
	"""
	Class contains tests for the notLoggedIn view, the docstrings of each test function 
	explain what is tested
	"""
	def test_notLoggedIn_view_without_authentication_register_link(self):
		"""If the user is not logged in, there should be a register link"""
		response = self.client.get(reverse('notLoggedIn'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Register")

	def test_notLoggedIn_view_without_authentication_about_link(self):
		"""If the user is not logged in, there should be a about link"""
		response = self.client.get(reverse('notLoggedIn'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "About")

	def test_notLoggedIn_view_without_authentication_log_in_link(self):
		"""If the user is not logged in, there should be a log-in link"""
		response = self.client.get(reverse('notLoggedIn'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Log-In")

	def test_notLoggedIn_view_without_authentication_appropiate_header(self):
		"""If the user is not logged in, there should be a appropiate message in the header"""
		response = self.client.get(reverse('notLoggedIn'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Hello adventurer you are not logged in!")

class LoginViewTests(TestCase):
	"""
	Class contains tests for the Login view, the docstrings of each test function 
	explain what is tested
	"""

	def test_login_view_without_authentication_register_link(self):
		"""If the user is not logged in, there should be a register link"""
		response = self.client.get(reverse('login'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Register")

	def test_login_view_without_authentication_about_link(self):
		"""If the user is not logged in, there should be a about link"""
		response = self.client.get(reverse('login'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "About")

	def test_login_view_without_authentication_log_in_link(self):
		"""If the user is not logged in, there should be a log-in link"""
		response = self.client.get(reverse('login'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Log-In")

	def test_login_view_without_authentication_appropiate_header(self):
		"""If the user is not logged in, there should be a appropiate message in the header"""
		response = self.client.get(reverse('login'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Hello adventurer you are not logged in!")

	def test_login_page_form_invalid_credentials_only_username(self):
		"""If invalid credentials are given, there is appropiate message"""
		response = self.client.post(reverse('login'), {'username':'test', 'password':''})
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Invalid login credentials")

	def test_login_page_form_invalid_credentials_only_password(self):
		"""If invalid credentials are given, there is appropiate message"""
		response = self.client.post(reverse('login'), {'username':'', 'password':'test'})
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Invalid login credentials")

	def test_login_page_form_invalid_credentials(self):
		"""If invalid credentials are given, there is appropiate message"""
		response = self.client.post(reverse('login'), {'username':'test', 'password':'test'})
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Invalid login credentials")

	def test_login_page_form_valid_credentials(self):
		"""Redirect to index if valid credentials are entered into the form"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		response = self.client.post(reverse('login'), {'username':'testUser', 'password':'test1234'})
		self.assertEqual(response.status_code,302)

class RegisterViewTests(TestCase):
	"""
	Class contains tests for the Register view, the docstrings of each test function 
	explain what is tested
	"""
	def test_register_view_without_authentication_register_link(self):
		"""If the user is not logged in, there should be a register link"""
		response = self.client.get(reverse('register'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Register")

	def test_register_view_without_authentication_about_link(self):
		"""If the user is not logged in, there should be a about link"""
		response = self.client.get(reverse('register'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "About")

	def test_register_view_without_authentication_log_in_link(self):
		"""If the user is not logged in, there should be a log-in link"""
		response = self.client.get(reverse('register'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Log-In")

	def test_register_view_without_authentication_appropiate_header(self):
		"""If the user is not logged in, there should be a appropiate message in the header"""
		response = self.client.get(reverse('register'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "Hello adventurer you are not logged in!")

	def test_register_view_form_invalid_only_user_credentials(self):
		"""
		If only user credentials are given, there is appropiate message, ie that there are 
		fields missing. ie form errors from avatar_form.
		"""
		response = self.client.post(reverse('register'), {'username':'test', 'password':'test'})
		self.assertEqual(response.status_code,200)
		self.assertFormError(response, 'avatar_form', 'nickname', 'This field is required.')
		self.assertFormError(response, 'avatar_form', 'bio', 'This field is required.')

	def test_register_view_form_invalid_only_avatar_fields(self):
		"""
		If only avatar credentials are given, there is appropiate message, ie that there are 
		fields missing. ie form errors from user_form
		"""
		response = self.client.post(reverse('register'), {'nickname':'test', 'bio':'test'})
		self.assertEqual(response.status_code,200)
		self.assertFormError(response, 'user_form', 'username', 'This field is required.')
		self.assertFormError(response, 'user_form', 'password', 'This field is required.')

	def test_register_view_form_valid_form(self):
		"""If valid form is given to the view, the thank you message is performed and a link is given"""
		response = self.client.post(reverse('register'), {'nickname':'test', 'bio':'test', 'email':'test@test.com', 'username':'test', 'password':'test'})
		self.assertEqual(response.status_code,200)

		#check for thank you message
		self.assertContains(response, "Thank you for registering!")
		# check for the link
		self.assertContains(response, "Return to the homepage.")

class LogoutViewTests(TestCase):
	"""
	Class contains tests for the Logout view, the docstrings of each test function 
	explain what is tested
	"""
	def test_logout_view_authenticated_logout(self):
		"""
		If a logged in user presses the logout link, he/she is logged out, and redirected
		to another page
		"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		# log in this user
		self.client.login(username="testUser", password="test1234")
		response = self.client.get(reverse('logout'))
		
		self.assertEqual(response.status_code, 302)

class AvatarProfileViewTests(TestCase):
	"""
	Class contains tests for the AvatarProfile view, the docstrings of each test function 
	explain what is tested
	"""

	def test_avatarProfile_status_check(self):
		"""
		This test checks the status code of the avatar page of a testuser + avatar
		created in this method.
		"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		self.client.login(username="testUser", password="test1234")
		response = self.client.get(reverse('avatar', args=('testname',)))
		self.assertEqual(response.status_code, 200)

	def test_avatarProfile_content_check(self):
		"""
		This test checks the contents of the avatar page of a testuser + avatar
		created in this method. In particular it checks for the name, and the 
		two important links of adding myquests and logging in hours
		"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		self.client.login(username="testUser", password="test1234")
		response = self.client.get(reverse('avatar', args=('testname',)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "TestName")
		self.assertContains(response, "Add MyQuest")
		self.assertContains(response, "Log in Hours")

	def test_avatarProfile_if_no_myquests(self):
		"""
		This test checks if there is an appropiate message if no myquests have been added to the
		avatar yet.
		"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		self.client.login(username="testUser", password="test1234")
		response = self.client.get(reverse('avatar', args=('testname',)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "TestName")
		self.assertContains(response, "Add MyQuest")
		self.assertContains(response, "Log in Hours")
		self.assertContains(response, "No myQuests currently in avatar. Create one for yourself! Self Challenge and Discipline is important!")

	def test_avatarProfile_authenticated_user(self):
		"""Test checks absence of message meant for unauthenticated users (users of type AnonymousUser)"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		self.client.login(username="testUser", password="test1234")
		response = self.client.get(reverse('avatar', args=('testname',)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "TestName")
		self.assertContains(response, "Add MyQuest")
		self.assertContains(response, "Log in Hours")
		self.assertNotContains(response, "Hello adventurer you are not logged in!")

	def test_avatarProfile_not_authenticated_user(self):
		"""Checks for redirect if user is not authenticated"""
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		# dont log in
		response = self.client.get(reverse('avatar', args=('testname',)))
		# check for the redirect
		self.assertEqual(response.status_code, 302)

	def test_avatarProfile_authenticated_user_but_not_users_avatar(self):
		"""
		This tests the case when the logged in user views an avatar profile that is not his/hers
		in particular it makes sure that myquest addition and logging hours is not possible
		"""
		# create a user
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		testUser2 = User.objects.create_user(username = "testUser2", email="test@test.com", password="test1234")
		testAvatar2 = Avatar(user=testUser2, nickname="TestName2", bio="Test Biography", confirm=True)
		testAvatar2.save()

		self.client.login(username="testUser2", password="test1234")
		response = self.client.get(reverse('avatar', args=('testname',)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "TestName")
		self.assertNotContains(response, "Add MyQuest")
		self.assertNotContains(response, "Log in Hours")


	def test_avatarProfile_if_myquest(self):
		"""
		This tests the avatar view if the logged in user owns the profile and there are myquests present
		In particular myquests should be displayed and the no myquests message should not be displayed
		"""
		# create a user + avatar
		testUser = User.objects.create_user(username = "testUser", email="test@test.com", password="test1234")
		testAvatar = Avatar(user=testUser, nickname="TestName", bio="Test Biography", confirm=True)
		testAvatar.save()

		# create a myQuest
		myQuest = MyQuest(avatar=testAvatar, title="TestTitle", description="Test Description", publish=False)
		myQuest.save()

		self.client.login(username="testUser", password="test1234")
		response = self.client.get(reverse('avatar', args=('testname',)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "TestName")
		self.assertContains(response, "Add MyQuest")
		self.assertContains(response, "Log in Hours")
		self.assertNotContains(response, "No myQuests currently in avatar. Create one for yourself! Self Challenge and Discipline is important!")

		num_myQuests = len(response.context['myQuests'])
		self.assertEqual(num_myQuests, 1)

