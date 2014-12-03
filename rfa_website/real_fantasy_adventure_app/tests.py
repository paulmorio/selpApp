from django.test import TestCase
from django.contrib.auth import get_user_model
from . models import Quest

# TestCases for Quest
class QuestEntryTest(TestCase):

	def test_create_unpublished(self):
		quest = Quest(title="Test Title", description="Test Description", publish=False)
		quest.save()
		self.assertEqual(Quest.objects.all().count(), 1)
		self.assertEqual(Quest.objects.published().count(), 0)
		quest.publish = True
		quest.save()
		self.assertEqual(Quest.objects.published().count(), 1)
