from abc import ABC, abstractmethod

class IAiAssistantService(ABC):
    @abstractmethod
    def init_chat(self, token: str, chat_id: str) -> dict:
        """Initialize chat sessions for all AI endpoints

        Args:
            token: Authentication token
            chat_id: Unique chat identifier

        Returns:
            dict: Success status of initialization
        """
        pass

    @abstractmethod
    def ai_chat(self, token: str, chat_id: str, ai_endpoint: str, ai_question: str) -> dict:
        """Send chat message to appropriate AI endpoint

        Args:
            token: Authentication token
            chat_id: Unique chat identifier
            ai_endpoint: Target AI endpoint to route message to, enum ['random', 'trino'], trino is used for data retrieval, data aggregation
            ai_question: Chat message/question to send

        Returns:
            dict: AI response message

        Raises:
            ValueError: If ai_endpoint is not recognized
        """
        pass

