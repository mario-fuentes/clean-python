from typing import List

from sqlalchemy.orm import Session

from app.entities.contact import Contact
from app.infra.orm.contact_mapper import ContactMapper
from app.repositories.alchemy.AlchemyContactsRepository import AlchemyContactsRepository
from app.test.repositories.alchemy.alchemy_test_base import AlchemyTestBase
from orm.i_entity_mapper import IEntityMapper


class TestAlchemyContactsRepository(AlchemyTestBase):
    def get_mappers(self) -> List[IEntityMapper]:
        return [ContactMapper()]

    def init_with_session(self, session: Session):
        self.repo = AlchemyContactsRepository(session)

    def test_save_should_persist_and_generate_the_id(self):
        contact = Contact('Marge Simpson',
                          '+1 23456789',
                          'marge@fox.com')

        self.repo.save(contact)
        self.flush()

        self.assertEqual(1, contact.id)

    def test_get_should_return_an_existing_instance(self):
        new_contact = Contact('Moe', '123', 'abc')
        self.repo.save(new_contact)
        self.flush()

        contact = self.repo.get(new_contact.id)
        self.assertIsNotNone(contact)
        self.assertEqual('Moe', contact.name)
        self.assertEqual('123', contact.phone)
        self.assertEqual('abc', contact.email)

    def test_get_all_should_return_all_contacts(self):
        self.repo.save(Contact('Pedro', '123', 'abc'))
        self.repo.save(Contact('Juan', '123', 'abc'))
        self.repo.save(Contact('Diego', '123', 'abc'))
        self.flush()

        contacts = self.repo.get_all()
        self.assertIsNotNone(contacts)
        self.assertEqual(3, len(contacts))
