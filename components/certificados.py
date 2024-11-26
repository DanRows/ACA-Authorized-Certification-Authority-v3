from datetime import datetime
from typing import Dict, List


class Certificados:
    def __init__(self):
        self._certificates = []

    def get_total(self) -> int:
        return len(self._certificates)

    def get_certificates(self) -> List[Dict]:
        return self._certificates

    def add_certificate(self, certificate: Dict) -> None:
        certificate['created_at'] = datetime.now()
        self._certificates.append(certificate)
