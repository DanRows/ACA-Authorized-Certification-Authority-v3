from datetime import datetime
import time
from contextlib import contextmanager

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        
    def record_metric(self, name: str, value: float):
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append({
            'value': value,
            'timestamp': datetime.now()
        })
        
    @contextmanager
    def measure_time(self, operation_name: str):
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.record_metric(operation_name, duration)
