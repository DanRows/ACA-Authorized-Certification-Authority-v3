# config/secrets_manager.py

import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

class SecretsManager:
    """
    Manages sensitive credentials securely.
    """

    @staticmethod
    def get_secret(key):
        """
        Retrieves a secret value from environment variables.

        Args:
            key (str): The name of the secret to retrieve.
        
        Returns:
            str: The secret value or None if not found.
        """
        return os.getenv(key)
