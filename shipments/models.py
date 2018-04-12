# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class Shipment(models.Model):
    timestamp = models.DateTimeField(default=datetime.now)
    # denormalize city for future query performance
    from_city = models.ForeignKey('City', related_name='sent_shipments', on_delete=models.PROTECT)
    from_street = models.ForeignKey('Street', related_name='sent_shipments', on_delete=models.PROTECT)
    from_address = models.CharField(max_length=64, null=True)

    dest_city = models.ForeignKey('City', related_name='received_shipments', on_delete=models.PROTECT)
    dest_street = models.ForeignKey('Street', related_name='received_shipments', on_delete=models.PROTECT)
    dest_address = models.CharField(max_length=64, null=True)
    deadline = models.DateTimeField(null=True)
    weight = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    client = models.ForeignKey('UserProfile', related_name='sent_shipments', on_delete=models.PROTECT)
    recipient = models.ForeignKey('UserProfile', related_name='received_shipments', on_delete=models.PROTECT)

    class Meta:
        db_table = 'shipment'

    def __str__(self):
        return u'{} {}'.format(self.timestamp, self.dest_city_id)


class City(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        db_table = 'city'

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=256)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    class Meta:
        db_table = 'street'

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=256, unique=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    MANAGER = 1
    CLIENT = 2

    USER_TYPES = [
        (MANAGER, u'manager'),
        (CLIENT, u'client'),
    ]

    user_type = models.SmallIntegerField(choices=USER_TYPES, default=CLIENT)

    class Meta:
        db_table = 'user_profile'
