import psutil
from opentelemetry.metrics import Observation, CallbackOptions
from typing import Iterable

def mem_percentage(options: CallbackOptions) -> Iterable[Observation]:

    memory_info = psutil.virtual_memory()
    mem_perc = memory_info.percent

    yield Observation(mem_perc, {})

def cpu_percentage(option: CallbackOptions) -> Iterable[Observation]:

    cpu_usage = psutil.cpu_percent(interval=1)

    yield Observation(cpu_usage, {})

def mem_total(option: CallbackOptions) -> Iterable[Observation]:

    memory_info = psutil.virtual_memory()
    mem_total = memory_info.total

    yield Observation(mem_total, {})

def mem_current(option: CallbackOptions)-> Iterable[Observation]:
    memory_info = psutil.virtual_memory()
    mem_c = memory_info.used

    yield Observation(mem_c, {})

class prometheus_metrics:
    def __init__(self, meter):

        self.total_requests = meter.create_counter(
            "api_total_requests", unit="1", description="Number of processed requests"
            )

        self.active_requests = meter.create_up_down_counter(
            "api_active_requests", unit = "1", description="Number of current active requests"
        )

        self.mem_perc = meter.create_observable_gauge(
            "mem_percentage", [mem_percentage]
        )

        self.cpu_perc = meter.create_observable_gauge(
            "cpu_percentage", [cpu_percentage]
        )

        self.mem_total = meter.create_observable_gauge(
            "mem_total", [mem_total]
        )

        self.mem_used = meter.create_observable_gauge(
            "mem_used", [mem_current]
        )

        

    def total_requests_add(self,value,endpoint):
        self.total_requests.add(
            value, attributes={"method":"GET", "endpoint": endpoint}
        )
    
    def active_requests_add(self, value):
        self.active_requests.add(value)
    
