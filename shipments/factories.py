import factory


class CityFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'city_{}'.format(n))
    class Meta:
        model = 'shipments.City'


class StreetFactory(factory.django.DjangoModelFactory):
    city = factory.SubFactory(CityFactory)
    name = factory.Sequence(lambda n: 'street_{}'.format(n))
    class Meta:
        model = 'shipments.Street'


class UserProfileFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: 'test_{}@test.test'.format(n))
    username = factory.Sequence(lambda n: 'username_{}'.format(n))
    class Meta:
        model = 'shipments.UserProfile'


class ShipmentFactory(factory.django.DjangoModelFactory):
    from_city = factory.LazyAttribute(lambda a: a.from_street.city)
    from_street = factory.SubFactory(StreetFactory)

    dest_city  = factory.LazyAttribute(lambda a: a.dest_street.city)
    dest_street = factory.SubFactory(StreetFactory)

    client = factory.SubFactory(UserProfileFactory)
    recipient = factory.SubFactory(UserProfileFactory)

    class Meta:
        model = 'shipments.Shipment'
