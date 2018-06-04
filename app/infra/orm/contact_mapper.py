from typing import Callable

from sqlalchemy import MetaData, Table, Column, Integer, String

from app.entities.contact import Contact
from orm.i_entity_mapper import IEntityMapper


class ContactMapper(IEntityMapper):
    def map(self, metadata: MetaData, mapper_func: Callable[[object, Table], None]):
        table = Table(
            'contact', metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('name', String(50), nullable=False),
            Column('phone', String(15), nullable=True),
            Column('email', String(100), nullable=True)
        )

        mapper_func(Contact, table)
