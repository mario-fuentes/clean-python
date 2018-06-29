import json
import os

from flask import Flask
from flask_injector import FlaskInjector
from flask_restful import Api
from sqlalchemy.orm import scoped_session

from app.configuration import configure_app_routes, configure_app_bindings, get_app_mappers
from orm.sqlalchemy_initializer import SQLAlchemyInitializer

routing_modules = [
    configure_app_routes
]

bindings_modules = [
    configure_app_bindings
]

mapping_modules = [
    get_app_mappers
]


def configure_database(config):
    initializer = SQLAlchemyInitializer(config['db_uri'])
    for module_mapper in mapping_modules:
        initializer.add_mappers(module_mapper())
    initializer.configure_database()
    return initializer


def get_version(config):
    return json.dumps({
        'version': config['version'],
        'commit': config['commit']
    })


def load_env_config(config):
    config['db_uri'] = os.getenv('APP_DB_URI', 'sqlite:///:memory:')
    config['version'] = os.getenv('DEPLOY_VERSION', 'NOT_DEFINED'),
    config['commit'] = os.getenv('COMMIT_REVISION', 'NOT_DEFINED')


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    load_env_config(app.config)

    initializer = configure_database(app.config)

    api = Api(app)
    for routing in routing_modules:
        routing(api)

    bindings_modules.append(initializer.get_inject_module(app))
    FlaskInjector(app=app, modules=bindings_modules)

    # a helper endpoint to identify the current version
    app.add_url_rule('/version', 'version', lambda: get_version(app.config))

    return app


# global instance required by the AWS Elastic Beanstalk
application = create_app()

if __name__ == "__main__":
    application.run(port=5000, threaded=True)
