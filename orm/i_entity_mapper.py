from abc import ABC, abstractmethod
from typing import Callable

from sqlalchemy import MetaData, Table


class IEntityMapper(ABC):
    @abstractmethod
    def map(self, metadata: MetaData, mapper_func: Callable[[object, Table], None]):
        pass
