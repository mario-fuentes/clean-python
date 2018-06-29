from unittest import TestCase
from unittest.mock import MagicMock

from sqlalchemy.orm import Session, mapper

from orm.i_entity_mapper import IEntityMapper
from orm.sqlalchemy_initializer import SQLAlchemyInitializer


class TestSQLAlchemyInitializer(TestCase):
    def setUp(self):
        self.initializer = SQLAlchemyInitializer('sqlite://')
        self.mock_mapper = MagicMock(IEntityMapper)

    def test_add_mapper_should_add_and_create_the_mapping(self):
        self.initializer.add_mapper(self.mock_mapper)
        self.initializer.configure_database()
        self.mock_mapper.map.assert_called_once_with(self.initializer.metadata, mapper)

    def test_add_mappers_should_add_and_create_the_mapping(self):
        self.initializer.add_mappers([self.mock_mapper, MagicMock()])
        self.initializer.configure_database()
        self.mock_mapper.map.assert_called_once_with(self.initializer.metadata, mapper)

    def test_configure_database_should_return_a_session_maker(self):
        session_maker = self.initializer.configure_database()
        self.assertIsNotNone(session_maker)
        self.assertEqual(session_maker, self.initializer.session_maker)

    def test_create_inject_module_should_return_a_new_instance(self):
        self.initializer.configure_database()
        module = self.initializer.get_inject_module(MagicMock())
        self.assertIsNotNone(module)
        session = module.provide_session()
        self.assertIsInstance(session, Session)
