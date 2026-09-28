from collections import defaultdict


class Metrics:

    def __init__(self):
        self.total_requests = 0
        self.total_client_errors = 0
        self.total_server_errors = 0
        self.total_duration = 0.0
        self.status_codes = defaultdict(int)

    def record_request(self, status_code: int, duration: float):
        self.total_requests += 1
        self.total_duration += duration
        self.status_codes[status_code] += 1

        if 400 <= status_code < 500:
            self.total_client_errors += 1

        elif status_code >= 500:
            self.total_server_errors += 1

    def get_metrics(self):
        average_duration = (
            self.total_duration / self.total_requests
            if self.total_requests
            else 0
        )

        return {
            "total_requests": self.total_requests,
            "total_client_errors": self.total_client_errors,
            "total_server_errors": self.total_server_errors,
            "average_response_time_ms": round(
                average_duration * 1000,
                2
            ),
            "status_codes": dict(self.status_codes),
        }


metrics = Metrics()