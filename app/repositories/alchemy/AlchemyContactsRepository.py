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

    def get(self, id: int) -> Contact:
        return self.session.query(Contact).get(id)

    def get_all(self) -> List[Contact]:
        return self.session.query(Contact).all()

    def get_by_name(self, name: str) -> List[Contact]:
        pass