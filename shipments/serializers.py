# -*- coding: utf-8 -*-

from shipments.models import Shipment, UserProfile, City, Street
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'user_type')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class StreetSerializer(serializers.ModelSerializer):
    full_title = serializers.SerializerMethodField()

    class Meta:
        model = Street
        fields = '__all__'

    def get_full_title(self, obj):
        return '{} - {}'.format(obj.name, obj.city.name)


class ShipmentSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    from_city = CitySerializer(read_only=True)
    dest_city = CitySerializer(read_only=True)
    from_street = StreetSerializer(read_only=True)
    dest_street = StreetSerializer(read_only=True)

    client_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), source='client', write_only=True)
    recipient_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), source='recipient', write_only=True)
    from_city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='from_city', write_only=True)
    dest_city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='dest_city', write_only=True)
    from_street_id = serializers.PrimaryKeyRelatedField(queryset=Street.objects.all(), source='from_street', write_only=True)
    dest_street_id = serializers.PrimaryKeyRelatedField(queryset=Street.objects.all(), source='dest_street', write_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
