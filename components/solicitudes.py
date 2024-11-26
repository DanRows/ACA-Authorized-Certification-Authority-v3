from datetime import datetime
from typing import Dict, List


class Solicitudes:
    def __init__(self):
        self._requests = []

    def get_total(self) -> int:
        return len(self._requests)

    def get_requests(self) -> List[Dict]:
        return self._requests

    def add_request(self, request: Dict) -> None:
        request['created_at'] = datetime.now()
        self._requests.append(request)
