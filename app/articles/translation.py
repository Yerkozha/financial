from modeltranslation.translator import translator, TranslationOptions

from .models import Article

class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)

translator.register(Article, ArticleTranslationOptions)