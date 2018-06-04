import json
from unittest import TestCase

from app.test.test_app import create_test_app


class TestContactResource(TestCase):
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

