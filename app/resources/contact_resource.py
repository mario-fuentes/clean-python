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
            self.logger.exception(ex)
            return {'error': ex.strerror}, 500
