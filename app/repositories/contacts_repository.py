from abc import ABC, abstractmethod

from typing import List

from app.entities.contact import Contact


class ContactsRepository(ABC):
    @abstractmethod
    def save(self, contact: Contact):
        pass

    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def get_all(self) -> List[Contact]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> List[Contact]:
        pass
