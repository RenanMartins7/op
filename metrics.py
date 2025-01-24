class prometheus_metrics:
    def __init__(self, meter)

        self.total_requests = meter.create_counter(
            "api_total_requests", unit="1", description="Number of processed requests"
            )

        self.active_requests = meter.creater_up_and_down_counter(
            "api_active_requests", unit = "1", description="Number of current active requests"
        )

    def total_requests_add(self,value,endpoint):
        self.total_requests.add(
            value, attributes={"method":"GET", "endpoint": endpoint}
        )
    
    def active_requests_add(self, value):
        self.active_requests.add(value)
