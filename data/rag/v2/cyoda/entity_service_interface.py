from abc import ABC, abstractmethod
from typing import List, Any

class EntityService(ABC):

    @abstractmethod
    def get_item(self, token: str, entity_model: str, entity_version: str, id: str) -> Any:
        """Retrieve a single item based on its ID."""
        pass

    @abstractmethod
    def get_items(self, token: str, entity_model: str, entity_version: str) -> List[Any]:
        """Retrieve multiple items based on their IDs."""
        pass

    @abstractmethod
    def get_single_item_by_condition(self, token: str, entity_model: str, entity_version: str, condition: Any) -> List[Any]:
        """Retrieve multiple items based on their IDs."""
        pass

    @abstractmethod
    def get_items_by_condition(self, token: str, entity_model: str, entity_version: str, condition: Any) -> List[Any]:
        """Retrieve multiple items based on their IDs."""
        pass

    @abstractmethod
    def add_item(self, token: str, entity_model: str, entity_version: str, entity: Any) -> Any:
        """Add a new item to the repository."""
        pass

    @abstractmethod
    def update_item(self, token: str, entity_model: str, entity_version: str, id: str, entity: Any, meta: Any) -> Any:
        """Update an existing item in the repository."""
        pass