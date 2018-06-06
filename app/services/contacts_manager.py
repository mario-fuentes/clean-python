from injector import inject

from app.entities.contact import Contact
from app.entities.exceptions import ValidationError
from app.infra.logger import Logger
from app.repositories.contacts_repository import ContactsRepository
from app.services.service_exception import ServiceException


class ContactsManager:
    @inject
    def __init__(self,
                 contacts_repository: ContactsRepository,
                 logger: Logger):
        self.repo = contacts_repository
        self.logger = logger

    def create_contact(self, name: str, phone: str, email: str):
        contact = Contact(name, phone, email)

        self._validate_contact(contact)
        self._add_contact(contact)

        return contact

    def get_contact_by_id(self, id: int):
        try:
            return self.repo.get(id)
        except Exception as ex:
            self.logger.exception(ex)
            raise ServiceException from ex

    def get_all(self):
        try:
            return self.repo.get_all()
        except Exception as ex:
            self.logger.exception(ex)
            raise ServiceException from ex

    def _validate_contact(self, contact: Contact):
        try:
            contact.validate()
        except ValidationError as ve:
            raise ServiceException from ve

    def _add_contact(self, contact: Contact):
        try:
            self.repo.save(contact)
        except Exception as ex:
            self.logger.exception(ex)
            raise ServiceException from ex
