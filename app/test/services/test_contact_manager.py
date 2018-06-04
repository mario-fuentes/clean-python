from unittest import TestCase
from unittest.mock import MagicMock

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

