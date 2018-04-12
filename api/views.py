# -*- coding: utf-8 -*-
from shipments.models import Shipment, UserProfile, Street, City
from rest_framework import viewsets
from shipments.serializers import ShipmentSerializer, UserSerializer, StreetSerializer, CitySerializer
from api.permissions import IsCreationOrIsAuthenticated
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsCreationOrIsAuthenticated]


class ShipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Shipment.objects.order_by('-id').select_related(
        'client', 'recipient', 'from_street__city', 'from_city',
        'dest_city', 'dest_street__city'
    )
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        params = self.request.query_params
        client_id = params.get('client_id')
        if client_id:
            self.queryset = self.queryset.filter(client=client_id)
        return self.queryset


class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer


class StreetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Street.objects.all().select_related('city')
    serializer_class = StreetSerializer
