from django.contrib import admin
from . import models
from django_markdown.admin import MarkdownModelAdmin

class QuestAdmin(MarkdownModelAdmin):
	list_display = ("title", "created_date")
	prepopulated_fields = {"slug": ("title",)} #automatically populates the slug with JavaScript in admin

# Register your models here.
admin.site.register(models.Quest, QuestAdmin)