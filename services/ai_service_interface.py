# services/ai_service_interface.py

from abc import ABC, abstractmethod

class AIServiceInterface(ABC):
    """
    Abstract base class for AI service integrations.
    """

    @abstractmethod
    def process_request(self, request_data):
        """
        Processes a user request and returns a response.

        Args:
            request_data (dict): The data for the request.

        Returns:
            dict: The response from the AI service.
        """
        pass
