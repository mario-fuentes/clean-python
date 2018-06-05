from injector import inject

from app.entities.contact import Contact
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

        self.__validate_contact(contact)
        self.__add_contact(contact)

        return contact

    def get_contact_by_id(self, id: int):
        return self.repo.get(id)

    def get_all(self):
        return self.repo.get_all()

    def __validate_contact(self, contact: Contact):
        if contact.name is None:
            raise ServiceException

    def __add_contact(self, contact: Contact):
        try:
            self.repo.save(contact)
        except Exception as ex:
            self.logger.exception(ex)
            raise ServiceException from ex
