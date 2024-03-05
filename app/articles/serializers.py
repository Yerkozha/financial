from rest_framework import serializers

from .models import Article

class ArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'source', 'image']
