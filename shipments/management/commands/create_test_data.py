import random
from datetime import date
from django.core.management.base import BaseCommand
from shipments.models import Shipment, UserProfile, City, Street
from shipments.utils import random_date

TEST_CITIES = [
    'Абакан',
    'Анапа',
    'Архангельск',
    'Астрахань',
    'Брянск',
    'Владивосток',
    'Владикавказ',
    'Владимир',
    'Москва',
]

TEST_STREETS = [
    'Большая Дмитровка',
    'Малая Дмитровка',
    'Юбилейная',
    'Ленина'
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('creating cities')
        for name in TEST_CITIES:
            city, _ = City.objects.get_or_create(name=name)
            print('creating streets for city {}'.format(name))
            for street in TEST_STREETS:
                Street.objects.get_or_create(city=city, name=street)

        print('creating users')
        for i in range(20):
            user, _ = UserProfile.objects.get_or_create(
                username='test_user_{}'.format(i),
                email='test_user_email_{}@test.test'.format(i)
            )
            user.set_password('123')
            user.save()

        streets_data = Street.objects.values('id', 'city')
        users_data = UserProfile.objects.values_list('id', flat=True)
        for i in range(100):
            st_data = random.choice(streets_data)
            st_data_from = random.choice(streets_data)
            Shipment.objects.create(
                deadline=None if random.random() > 0.5 else random_date(date(2018,4,1), date(2018,6,1)),
                client_id=random.choice(users_data),
                recipient_id=random.choice(users_data),
                from_address='{}-{}'.format(random.randint(1,50), random.randint(1,300)),
                dest_address='{}-{}'.format(random.randint(1,50), random.randint(1,300)),
                dest_city_id=st_data['city'],
                dest_street_id=st_data['id'],
                from_city_id=st_data_from['city'],
                from_street_id=st_data_from['id'],
                weight=random.randint(1, 300)
            )

