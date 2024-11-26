# components/certificados.py

class Certificados:
    """
    Handles certificate-related operations.
    """

    def generate_certificate(self, user_data):
        """
        Generates a certificate based on user data.

        Args:
            user_data (dict): Data of the user for the certificate.

        Returns:
            str: The path to the generated certificate.
        """
        return f"Certificate for {user_data['name']} created!"
