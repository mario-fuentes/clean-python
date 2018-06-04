from flask import Flask
from flask_injector import FlaskInjector
from flask_restful import Api

from app.configuration import configure_app_routes, configure_app_bindings, get_app_mappers
from orm.sqlalchemy_initializer import SQLAlchemyInitializer


def create_test_app(modules=None):
    app = Flask(__name__)
    initializer = SQLAlchemyInitializer(db_uri='sqlite:///:memory:')
    initializer.add_mappers(get_app_mappers())
    initializer.configure_database()
    modules = modules or [configure_app_bindings]
    modules.append(initializer.get_inject_module())

    api = Api(app)
    configure_app_routes(api)

    FlaskInjector(app=app, modules=modules)
    return app
