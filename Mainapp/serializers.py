from rest_framework import serializers
from .models import customer, counselor


class customerSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer
        fields = ('cu_id', 'pw', 'name', 'phone')

class counselorSerializer(serializers.ModelSerializer):
    class Meta:
        model = counselor
        fields = ('co_id', 'pw', 'name', 'phone')
