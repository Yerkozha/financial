from django.contrib import admin

from .models import Article
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin

class ArticleAdminTranslation(TranslationAdmin):
    list_display = ("id", "title", "content", "image", "source",)


admin.site.register(Article, ArticleAdminTranslation)