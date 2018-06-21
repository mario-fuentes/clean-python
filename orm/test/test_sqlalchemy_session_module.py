from unittest import TestCase

from sqlalchemy.orm import Session, scoped_session

from orm.sqlalchemy_session_module import SQLAlchemySessionModule


class TestSqlAlchemySessionModule(TestCase):
    def setUp(self):
        session_factory = lambda: Session()
        self.provider = SQLAlchemySessionModule(session_factory)

    def test_provide_session_when_called_then_should_return(self):
        session = self.provider.provide_session()

        self.assertIsNotNone(session)
        self.assertIsInstance(session, Session)

    def test_provide_scoped_session_factory_should_return_an_instance(self):
        session = self.provider.provide_scoped_session_factory()

        self.assertIsNotNone(session)
        self.assertIsInstance(session, scoped_session)
