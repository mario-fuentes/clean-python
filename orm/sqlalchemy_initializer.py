from typing import List

from injector import Module
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import clear_mappers, mapper, sessionmaker

from orm.i_entity_mapper import IEntityMapper
from orm.sqlalchemy_session_module import SQLAlchemySessionModule


class SQLAlchemyInitializer:

    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri, convert_unicode=True)
        self.metadata = MetaData(self.engine)
        self.entity_mappers = []
        self.session_maker = None
        self.clear()

    def clear(self):
        clear_mappers()

    def add_mapper(self, entity_mapper: IEntityMapper):
        self.entity_mappers.append(entity_mapper)

    def add_mappers(self, mappers: List[IEntityMapper]):
        for _mapper in mappers:
            self.add_mapper(_mapper)

    def __create_mapping__(self):
        for _mapper in self.entity_mappers:
            _mapper.map(self.metadata, mapper)

    def configure_database(self):
        self.__create_mapping__()
        self.metadata.create_all()
        self.session_maker = sessionmaker(bind=self.engine)
        return self.session_maker

    def get_inject_module(self) -> Module:
        return SQLAlchemySessionModule(self.session_maker)
