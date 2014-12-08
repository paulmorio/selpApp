from django.test import TestCase
from django.contrib.auth import get_user_model
from . models import Quest, Avatar

# TestCases for Quest Entries
class QuestEntryTest(TestCase):

	def test_create_unpublished(self):
		quest = Quest(title="Test Title", description="Test Description", publish=False)
		quest.save()
		self.assertEqual(Quest.objects.all().count(), 1)
		self.assertEqual(Quest.objects.published().count(), 0)
		quest.publish = True
		quest.save()
		self.assertEqual(Quest.objects.published().count(), 1)

# TestCases for Avatar Entries
class AvatarEntryTest(TestCase):

	def test_create_unconfirmed(self):
		avatar = Avatar(name="TestName", bio="Test Biography", confirm=False)
		avatar.save()
		self.assertEqual(Avatar.objects.all().count(), 1)
		self.assertEqual(Avatar.objects.confirmed().count(), 0)
		avatar.confirm = True
		avatar.save()
		self.assertEqual(Avatar.objects.confirmed().count(), 1)


