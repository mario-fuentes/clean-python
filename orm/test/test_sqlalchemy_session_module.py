from unittest import TestCase
from unittest.mock import MagicMock

from flask import Flask
from sqlalchemy.orm import Session, scoped_session

from orm.sqlalchemy_session_module import SQLAlchemySessionModule


class TestSqlAlchemySessionModule(TestCase):
    def setUp(self):
        session_factory = lambda: Session()
        self.app: Flask = MagicMock()
        self.provider = SQLAlchemySessionModule(session_factory, self.app)

    def test_provide_session_when_called_then_should_return(self):
        session = self.provider.provide_session()

        self.assertIsNotNone(session)
        self.assertIsInstance(session, Session)

    def test_provide_scoped_session_factory_should_return_an_instance(self):
        session = self.provider.provide_scoped_session_factory()

        self.assertIsNotNone(session)
        self.assertIsInstance(session, scoped_session)

    def test_init_should_connect_to_the_teardown_request_event(self):
        self.app.teardown_request.assert_called_once()