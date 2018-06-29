from flask import Flask
from injector import Module, provider
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class SQLAlchemySessionModule(Module):
    def __init__(self, session_factory: sessionmaker, app: Flask):
        self.scoped_factory: scoped_session = scoped_session(session_factory)

        # Injector will inject automatically the Session into the context
        @app.teardown_request
        def shutdown_session(sender, exception=None, session_manager: scoped_session = None):
            session_manager.remove()

    @provider
    def provide_session(self) -> Session:
        return self.scoped_factory()

    @provider
    def provide_scoped_session_factory(self) -> scoped_session:
        return self.scoped_factory
