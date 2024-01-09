from django.http import HttpResponse
from .models import Financial
from rest_framework import viewsets
from .serializers import FinancialModelSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .tasks import update_news


class FinancialViewSet(viewsets.GenericViewSet):
    queryset = Financial.objects.all()
    serializer_class = FinancialModelSerializer
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=['post'])
    def create_financial(self, request, pk=None):

        print(request.data, '\n====================')
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)


        data = serializer.validated_data

        is_exists = Financial.objects.filter(bin=data['bin']).first()

        if is_exists is None:

            serializer.save()

            return Response(serializer.data)

        return Response('Already existing record', status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



