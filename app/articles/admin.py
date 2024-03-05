from django.contrib import admin

from .models import Article
from django.utils.translation import gettext_lazy as _

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display =  ("title", "content", "image", "source", )