from flask_restful import Api
from injector import Binder
from typing import List

from app.infra.orm.contact_mapper import ContactMapper
from app.repositories.alchemy.AlchemyContactsRepository import AlchemyContactsRepository
from app.repositories.contacts_repository import ContactsRepository
from app.resources.contact_resource import ContactResource
from orm.i_entity_mapper import IEntityMapper


def configure_app_routes(api: Api):
    api.add_resource(ContactResource,
                     '/contacts',
                     '/contacts/<int:id>')


def configure_app_bindings(binder: Binder):
    binder.bind(ContactsRepository, AlchemyContactsRepository)


def get_app_mappers() -> List[IEntityMapper]:
    return [
        ContactMapper(),
    ]
