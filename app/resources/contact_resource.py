from flask import request
from flask_restful import Resource, fields, marshal
from injector import inject
from sqlalchemy.orm import Session

from app.infra.logger import Logger
from app.services.contacts_manager import ContactsManager
from app.services.service_exception import ServiceException

__contact_fields__ = {
    'id': fields.Integer,
    'name': fields.String,
    'phone': fields.String,
    'email': fields.String
}


class ContactResource(Resource):
    @inject
    def __init__(self,
                 manager: ContactsManager,
                 logger: Logger,
                 session: Session):
        self.manager = manager
        self.logger = logger
        self.session = session

    def post(self):
        params = request.get_json()

        if not params:
            return {}, 400

        try:
            contact = self.manager.create_contact(params['name'],
                                                  params['phone'],
                                                  params['email'])
            self.session.commit()

            return marshal(contact, __contact_fields__), 201
        except ServiceException as ex:
            self.session.rollback()
            return self._create_exception_response(ex)

    def get(self, id: int = None):

        if not id:
            return self._get_all()

        return self._get_by_id(id)

    def _get_all(self):
        try:
            contacts = self.manager.get_all()
            return marshal(contacts, __contact_fields__), 200
        except ServiceException as ex:
            return self._create_exception_response(ex)

    def _get_by_id(self, id: int):
        if id <= 0:
            return {}, 400

        try:
            contact = self.manager.get_contact_by_id(id)

            return marshal(contact, __contact_fields__), 200
        except ServiceException as ex:
            return self._create_exception_response(ex)

    def _create_exception_response(self, ex: ServiceException):
        self.logger.exception(ex)
        return {'error': str(ex)}, 500