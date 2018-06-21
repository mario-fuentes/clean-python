from injector import Module, provider
from sqlalchemy.orm import Session, scoped_session


class SQLAlchemySessionModule(Module):
    def __init__(self, session_factory):
        self.scoped_factory: scoped_session = scoped_session(session_factory)

    @provider
    def provide_session(self) -> Session:
        return self.scoped_factory()

    @provider
    def provide_scoped_session_factory(self) -> scoped_session:
        return self.scoped_factory
