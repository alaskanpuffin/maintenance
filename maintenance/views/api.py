from ..models import Asset, Model
from rest_framework import viewsets
from rest_framework import permissions
from ..serializers import AssetSerializer, ModelSerializer


class AssetApiViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all().order_by('-updated')
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]

class ModelApiViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all().order_by('-updated')
    serializer_class = ModelSerializer
    permission_classes = [permissions.IsAuthenticated]
