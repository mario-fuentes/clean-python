from typing import List

from injector import inject
from sqlalchemy.orm import Session

from app.entities.contact import Contact
from app.repositories.contacts_repository import ContactsRepository


class AlchemyContactsRepository(ContactsRepository):
    @inject
    def __init__(self, session: Session):
        self.session = session

    def save(self, contact: Contact):
        self.session.add(contact)

    def get(self, id: int):
        pass

    def get_all(self) -> List[Contact]:
        pass

    def get_by_name(self, name: str) -> List[Contact]:
        pass