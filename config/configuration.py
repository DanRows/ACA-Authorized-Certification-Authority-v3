# config/configuration.py

class Configuration:
    """
    Centralized configuration class for the ACMA Dashboard.
    """

    def __init__(self):
        self.settings = {
            "database_url": "postgresql://user:password@localhost/acma_db",
            "ai_providers": ["openai", "vertex", "sambanova"],
            "default_provider": "openai",
        }

    def get_setting(self, key):
        """
        Retrieves a setting by key.

        Args:
            key (str): The configuration key.

        Returns:
            Any: The value associated with the key.
        """
        return self.settings.get(key, None)
