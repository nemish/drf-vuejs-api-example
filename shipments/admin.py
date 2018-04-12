from django.contrib import admin

from .models import City, Street, Shipment, UserProfile

admin.site.register(City)
admin.site.register(Street)
admin.site.register(Shipment)
admin.site.register(UserProfile)

# Register your models here.
