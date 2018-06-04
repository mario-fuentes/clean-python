from abc import ABC, abstractmethod
from unittest import TestCase

from typing import List

from sqlalchemy.orm import Session

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
