import json
from unittest import TestCase

from app.test.test_app import create_test_app


class TestContactResourceIntegration(TestCase):

    def setUp(self):
        self.app = create_test_app()
        self.client = self.app.test_client()

    def test_post_should_create_and_persist_a_new_contact(self):
        data = json.dumps({
            'name': 'Lisa Simpson',
            'phone': None,
            'email': 'lisa@fox.com'
        })

        response = self.client.post('/contacts',
                                    data=data,
                                    content_type='application/json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response.json['id'])
        self.assertEqual('Lisa Simpson', response.json['name'])
        self.assertEqual('lisa@fox.com', response.json['email'])

    def test_get_should_retrieve_a_contact_by_id(self):
        data = json.dumps({
            'name': 'Bart Simpson',
            'phone': '123456789',
            'email': 'bart@fox.com'
        })

        response = self.client.post('/contacts',
                                    data=data,
                                    content_type='application/json')

        self.assertEqual(201, response.status_code)

        response = self.client.get(str.format('/contacts/{}', response.json['id']))

        self.assertEqual(200, response.status_code)
        self.assertEqual('Bart Simpson', response.json['name'])
        self.assertEqual('123456789', response.json['phone'])
        self.assertEqual('bart@fox.com', response.json['email'])

    def test_get_should_retrieve_all_contacts(self):
        for i in range(5):
            r = self.client.post('/contacts',
                                 data=json.dumps({
                                     'name': str.format('user{}', i),
                                     'phone': None,
                                     'email': None
                                 }),
                                 content_type='application/json')
            self.assertEqual(201, r.status_code)

        response = self.client.get('/contacts')

        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.json))

    def test_get_should_retrieve_an_empty_list_when_doesnt_exists_any_contact(self):
        response = self.client.get('/contacts')

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.json))
