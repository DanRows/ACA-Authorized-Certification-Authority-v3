from datetime import datetime, timedelta
from typing import Dict, List

from components.certificados import Certificados
from components.solicitudes import Solicitudes
from utils.cache import cached


class MetricsService:
    def __init__(self):
        self.solicitudes = Solicitudes()
        self.certificados = Certificados()

    @cached(ttl=3600)
    def get_metrics(self) -> Dict:
        return {
            "total_solicitudes": self.solicitudes.get_total(),
            "total_certificados": self.certificados.get_total()
        }

    def get_dashboard_metrics(self, days: int) -> Dict:
        return {
            "total_requests": self.solicitudes.get_total(),
            "pending_requests": self._get_pending_requests(),
            "total_certificates": self.certificados.get_total(),
            "success_rate": self._calculate_success_rate(),
            "daily_metrics": self._get_daily_metrics(days),
            "provider_stats": self._get_provider_stats()
        }

    def _get_pending_requests(self) -> int:
        return len([r for r in self.solicitudes.get_requests()
                   if r['status'] == 'pending'])

    def _calculate_success_rate(self) -> float:
        requests = self.solicitudes.get_requests()
        if not requests:
            return 100.0
        completed = len([r for r in requests if r['status'] == 'completed'])
        return round((completed / len(requests)) * 100, 2)

    def _get_daily_metrics(self, days: int) -> Dict:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return {
            "requests": self._get_daily_requests(start_date, end_date),
            "certificates": self._get_daily_certificates(start_date, end_date)
        }

    def _get_provider_stats(self) -> Dict:
        return {
            'openai': 40,
            'vertex': 35,
            'sambanova': 25
        }

    def _get_daily_requests(self, start_date: datetime, end_date: datetime) -> Dict:
        requests = self.solicitudes.get_requests()
        # Implementar lógica real aquí
        return {}

    def _get_daily_certificates(self, start_date: datetime, end_date: datetime) -> Dict:
        certificates = self.certificados.get_certificates()
        # Implementar lógica real aquí
        return {}
