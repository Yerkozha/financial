from rest_framework import serializers
from .models import Financial


class FinancialModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Financial
        fields = '__all__'
