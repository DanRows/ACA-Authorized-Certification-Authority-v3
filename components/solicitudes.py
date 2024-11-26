# components/solicitudes.py

class Solicitudes:
    """
    Handles the management and processing of requests in the ACMA Dashboard.
    """

    def __init__(self):
        self.requests = []

    def add_request(self, user_data, request_type):
        """
        Adds a new request to the system.

        Args:
            user_data (dict): Information about the user making the request.
            request_type (str): Type of the request (e.g., "certificate", "query").
        
        Returns:
            dict: A confirmation message with the request ID.
        """
        request_id = len(self.requests) + 1
        new_request = {
            "id": request_id,
            "user_data": user_data,
            "type": request_type,
            "status": "pending",
        }
        self.requests.append(new_request)
        return {"message": "Request added successfully", "request_id": request_id}

    def get_requests(self):
        """
        Retrieves all the requests in the system.

        Returns:
            list: A list of all requests.
        """
        return self.requests
