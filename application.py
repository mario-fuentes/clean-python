import json
import os

from flask import Flask
from flask_injector import FlaskInjector
from flask_restful import Api

from orm.sqlalchemy_initializer import SQLAlchemyInitializer

routing_modules = []

bindings_modules = []

mapping_modules = []


def configure_database(config):
    initializer = SQLAlchemyInitializer(config['db_uri'])
    for module_mapper in mapping_modules:
        initializer.add_mappers(module_mapper())
    initializer.configure_database()
    return initializer


def get_version():
    return json.dumps({
        'version': os.getenv('DEPLOY_VERSION'),
        'commit': os.getenv('COMMIT_REVISION')
    })


def create_app():
    app = Flask(__name__)

    initializer = configure_database(app.config)

    api = Api(app)
    for routing in routing_modules:
        routing(api)

    bindings_modules.append(initializer.get_inject_module())
    FlaskInjector(app=app, modules=bindings_modules)

    app.add_url_rule('/version', 'version', (lambda: get_version(app.config)))

    return app


# global instance required by the AWS Elastic Beanstalk
application = create_app()

if __name__ == "__main__":
    application.run(port=5000, threaded=True)
