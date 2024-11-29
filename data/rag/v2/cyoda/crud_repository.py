from abc import abstractmethod
from enum import Enum
from typing import List, Any, Optional

from common.repository.repository import Repository


class DBKeys(Enum):
    CYODA = "CYODA"

class CrudRepository(Repository):
    """
    Abstract base class defining a repository interface for CRUD operations.
    """
    @abstractmethod
    def get_meta(self, *args, **kwargs):
        return {}

    @abstractmethod
    def count(self, meta) -> int:
        """
        Returns the number of entities available.
        """
        pass

    @abstractmethod
    def delete(self, meta, entity: Any) -> None:
        """
        Deletes a given entity.
        """
        pass

    @abstractmethod
    def delete_all(self, meta) -> None:
        """
        Deletes all entities managed by the repository.
        """
        pass

    @abstractmethod
    def delete_all_entities(self, meta, entities: List[Any]) -> None:
        """
        Deletes the given entities.
        """
        pass

    @abstractmethod
    def delete_all_by_key(self, meta, keys: List[Any]) -> None:
        """
        Deletes all instances of the type T with the given keys.
        """
        pass

    @abstractmethod
    def delete_by_key(self, meta, key: Any) -> None:
        """
        Deletes the entity with the given key.
        """
        pass

    @abstractmethod
    def exists_by_key(self, meta, key: Any) -> bool:
        """
        Returns whether an entity with the given key exists.
        """
        pass

    @abstractmethod
    def find_all(self, meta) -> List[Any]:
        """
        Returns all instances of the type.
        """
        pass

    @abstractmethod
    def find_all_by_key(self, meta, keys: List[Any]) -> List:
        """
        Returns all instances of the type T with the given keys.
        """
        pass

    @abstractmethod
    def find_by_key(self, meta, key: Any) -> Optional[Any]:
        """
        Retrieves an entity by its key.
        """
        pass

    @abstractmethod
    def find_by_id(self, meta, uuid: Any) -> Optional[Any]:
        """
        Retrieves an entity by its technical id.
        """
        pass

    @abstractmethod
    def find_all_by_criteria(self, meta, criteria: Any) -> Optional[Any]:
        """
        Retrieves an entity by its technical id.
        """
        pass

    @abstractmethod
    def save(self, meta, entity: Any) -> Any:
        """
        Saves a given entity.
        """
        pass

    @abstractmethod
    def save_all(self, meta, entities: List[Any]) -> List[Any]:
        """
        Saves all given entities.
        """
        pass

    @abstractmethod
    def update(self, meta, id, entity: Any) -> Any:
        """
        Saves all given entities.
        """
        pass

    @abstractmethod
    def update_all(self, meta, entities: List[Any]) -> List[Any]:
        """
        Saves all given entities.
        """
        pass