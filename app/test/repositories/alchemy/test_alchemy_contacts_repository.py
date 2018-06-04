from abc import ABC, abstractmethod
from unittest import TestCase

from typing import List

from sqlalchemy.orm import Session

from app.entities.contact import Contact
from app.infra.orm.contact_mapper import ContactMapper
from app.repositories.alchemy.AlchemyContactsRepository import AlchemyContactsRepository
from orm.i_entity_mapper import IEntityMapper
from orm.sqlalchemy_initializer import SQLAlchemyInitializer


class AlchemyTestBase(TestCase, ABC):
    @abstractmethod
    def get_mappers(self) -> List[IEntityMapper]:
        pass

    @abstractmethod
    def init_with_session(self, session: Session):
        pass

    def setUp(self):
        self.initializer = SQLAlchemyInitializer(db_uri='sqlite:///:memory:')
        self.initializer.add_mappers(self.get_mappers())
        self.session_factory = self.initializer.configure_database()
        self.session: Session = self.session_factory()
        self.init_with_session(self.session)

    def tearDown(self):
        self.session.rollback()
        self.initializer.clear()

    def flush(self):
        self.session.flush()


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
