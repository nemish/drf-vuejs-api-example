import json
from django.test import TestCase, Client
from shipments.factories import ShipmentFactory, StreetFactory, UserProfileFactory
from shipments.models import Shipment


client = Client()


class RetrieveShipmentTestCase(TestCase):
    def setUp(self):
        self.shipment = ShipmentFactory()
        self.shipment2 = ShipmentFactory()

    def test_retrieve_ok(self):
        resp = client.get('/shipments/')
        self.assertEquals(resp.status_code, 200)

    def test_retrieve_as_pager(self):
        resp = client.get('/shipments/')
        resp_keys = set(resp.json().keys())
        self.assertEquals(resp_keys, {'pager', 'count', 'results'})

    def test_retrieve_all(self):
        resp = client.get('/shipments/')
        self.assertEquals(len(resp.json()['results']), 2)

    def test_retrieve_for_single_client(self):
        resp = client.get('/shipments/?client_id={}'.format(self.shipment.client_id))
        results = resp.json()['results']
        self.assertEquals(len(results), 1)
        item = results[0]
        self.assertEquals(item['id'], self.shipment.client_id)

    def test_retrieve_single_record(self):
        resp = client.get('/shipments/{}/'.format(self.shipment.pk))
        self.assertEquals(resp.json()['id'], self.shipment.pk)


class CreateShipmentTestCase(TestCase):

    def setUp(self):
        self.street = StreetFactory()
        self.dest_street = StreetFactory()
        self.client_user = UserProfileFactory()
        self.recipient_user = UserProfileFactory()

    def test_create_new(self):
        self.assertFalse(Shipment.objects.count())
        resp = client.post('/shipments/', data={
            'from_city_id': self.street.city_id,
            'from_street_id': self.street.pk,
            'dest_city_id': self.dest_street.city_id,
            'dest_street_id': self.dest_street.pk,
            'client_id': self.client_user.pk,
            'recipient_id': self.recipient_user.pk,
        })
        self.assertEquals(resp.status_code, 201)

        shipment = Shipment.objects.get()
        self.assertEquals(shipment.client_id, self.client_user.pk)


class UpdateShipmentTestCase(TestCase):

    def setUp(self):
        self.shipment = ShipmentFactory()

    def test_update(self):
        test_weight = 100
        client.patch('/shipments/{}/'.format(self.shipment.pk), data=json.dumps({
            'weight': 100
        }), content_type='application/json')

        self.shipment.refresh_from_db()
        self.assertEquals(self.shipment.weight, test_weight)


class DeleteShipmentTestCase(TestCase):

    def setUp(self):
        self.shipment = ShipmentFactory()

    def test_delete(self):
        self.assertTrue(Shipment.objects.exists())
        client.delete('/shipments/{}/'.format(self.shipment.pk))
        self.assertFalse(Shipment.objects.exists())
