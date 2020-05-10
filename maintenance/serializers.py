from .models import Asset, Model
from rest_framework import serializers

class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'name']

class AssetSerializer(serializers.HyperlinkedModelSerializer):
    model = ModelSerializer()
    class Meta:
        model = Asset
        fields = ['id', 'name', 'tag', 'model']
