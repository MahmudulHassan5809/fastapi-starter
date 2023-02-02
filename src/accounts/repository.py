from abc import ABC, abstractmethod
from src.accounts.models import User, UserCreate, UserUpdate

class UserAbstractRepo(ABC):
    @abstractmethod
    def create(self, user: UserCreate) -> User:
        raise NotImplementedError
    

    @abstractmethod
    def update(self, user: UserUpdate) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def all(self) -> list[User]:
        raise NotImplementedError
    

    @abstractmethod
    def delete(self, user_id: int) -> None:
        raise NotImplementedError


class UserRepo(UserAbstractRepo):
    pass