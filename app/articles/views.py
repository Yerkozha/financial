from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Article
from .serializers import (ArticlesSerializer)

from django.utils import translation # CHECK

class ArticlesViewSet(viewsets.GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticlesSerializer

    # def get_queryset(self):
    #     queryset = Article.objects.all()
    #     if 'HTTP_ACCEPT_LANGUAGE' in self.request.META:
    #         lang = self.request.META['HTTP_ACCEPT_LANGUAGE']
    #         translation.activate(lang)
    #     return queryset

    def get_permissions(self):
        if self.action == 'list_articles':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], parser_classes=(MultiPartParser, FormParser,))
    def create_article(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=True)


        serializer.save()
        status_code = status.HTTP_201_CREATED
        print(serializer.validated_data)
        print(serializer.data)
        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'User successfully registered!',
            'article': serializer.data
        }

        return Response(response, status=status_code)

    @action(detail=False, methods=['get'])
    def list_articles(self, request):
        serializer = self.get_serializer(Article.objects.all(), many=True)
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        print("accept_language", accept_language)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched users',
            'articles': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)





