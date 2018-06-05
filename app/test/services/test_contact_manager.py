from unittest import TestCase
from unittest.mock import MagicMock

from app.entities.contact import Contact
from app.infra.logger import Logger
from app.repositories.contacts_repository import ContactsRepository
from app.services.contacts_manager import ContactsManager
from app.services.service_exception import ServiceException


class TestContactManager(TestCase):
    def setUp(self):
        self.repo: ContactsRepository = MagicMock()
        self.manager = ContactsManager(self.repo, MagicMock(Logger))

    def test_create_contact_should_persist_a_new_instance(self):
        self.manager.create_contact('a', 'b', 'c')
        self.repo.save.assert_called_once()

    def test_create_contact_without_name_should_fire_an_exception(self):
        self.assertRaises(
                ServiceException,
                lambda: self.manager.create_contact(None, 'b', 'c'))

    def test_get_contact_by_id_should_return_an_instance_when_exists(self):
        self.repo.get.return_value = Contact('Moe')

        contact = self.manager.get_contact_by_id(1)

        self.assertIsNotNone(contact)
        self.assertEqual('Moe', contact.name)

    def test_get_all_should_return_all_contacts(self):
        self.repo.get_all.return_value = [
            Contact('A'),
            Contact('B'),
            Contact('C'),
        ]

        contacts = self.manager.get_all()

        self.assertIsNotNone(contacts)
        self.assertEqual(3, len(contacts))

