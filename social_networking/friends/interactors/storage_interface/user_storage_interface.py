from abc import ABC, abstractmethod
from typing import List


class UserStorageInterface(ABC):

    @abstractmethod
    def validate_email_id(self, email_id: str):
        pass

    @abstractmethod
    def validate_user_password(self, email_id: str, password: str):
        pass

    @abstractmethod
    def create_user(self, email_id: str, password: str, name: str):
        pass

    @abstractmethod
    def get_users_by_name(self, search_query: str, limit: int, offset: int):
        pass

    @abstractmethod
    def validate_user_ids(self, user_ids: List[str]):
        pass
