import json
from unittest import TestCase
from unittest.mock import MagicMock

from injector import Binder

from app.infra.orm.contact_mapper import ContactMapper
from app.services.contacts_manager import ContactsManager
from app.services.service_exception import ServiceException
from app.test.test_app import create_test_app


class TestContactResource(TestCase):
    def bind(self, binder: Binder):
        self.mock_manager: ContactsManager = MagicMock(ContactsManager)
        binder.bind(ContactsManager, to=self.mock_manager)

    def setUp(self):
        self.app = create_test_app([self.bind])
        self.client = self.app.test_client()

    def test_get_should_return_400_when_a_managed_exception_is_raised(self):
        self.mock_manager.get_all.side_effect = ServiceException('')

        response = self.client.get('/contacts')

        self.assertEqual(500, response.status_code)
        self.assertEqual('', response.json['error'])
