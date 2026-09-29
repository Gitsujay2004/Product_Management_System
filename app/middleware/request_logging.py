import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.metrics import metrics


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        monitoring_paths = {
            "/api/v1/health",
            "/api/v1/health/liveness",
            "/api/v1/health/readiness",
            "/api/v1/health/metrics",
        }

        if request.url.path not in monitoring_paths:
            metrics.record_request(
                response.status_code,
                process_time
            )

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "[request_id=%s] %s %s | %s | %.2fms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            process_time * 1000,
        )

        return response