from flask_injector import request
from injector import Module, provider
from sqlalchemy.orm import Session


class SQLAlchemySessionModule(Module):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    @request
    @provider
    def provide_session(self) -> Session:
        return self.session_factory()
