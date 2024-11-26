# services/factory.py

from services.openai_service import OpenAIService

class ServiceFactory:
    """
    Factory class to instantiate AI services dynamically.
    """

    @staticmethod
    def create_service(provider):
        """
        Creates an instance of an AI service based on the provider.

        Args:
            provider (str): The name of the provider (e.g., "openai").

        Returns:
            AIServiceInterface: An instance of the selected provider.
        """
        if provider == "openai":
            return OpenAIService()
        else:
            raise ValueError(f"Unsupported provider: {provider}")
