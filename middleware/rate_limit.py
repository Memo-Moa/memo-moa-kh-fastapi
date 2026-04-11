import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, uuid_limit: int = 1, ip_limit: int = 10, window: int = 60):
        super().__init__(app)
        self.uuid_limit = uuid_limit
        self.ip_limit = ip_limit
        self.window = window
        self.uuid_requests: dict[str, list[float]] = defaultdict(list)
        self.ip_requests: dict[str, list[float]] = defaultdict(list)

    def _cleanup(self, records: dict[str, list[float]]) -> None:
        now = time.time()
        expired_keys = []
        for key, timestamps in records.items():
            records[key] = [t for t in timestamps if now - t < self.window]
            if not records[key]:
                expired_keys.append(key)
        for key in expired_keys:
            del records[key]

    def _check_limit(
        self, key: str, records: dict[str, list[float]], limit: int
    ) -> tuple[bool, int]:
        now = time.time()
        timestamps = records[key]
        timestamps[:] = [t for t in timestamps if now - t < self.window]
        if len(timestamps) >= limit:
            oldest = timestamps[0]
            retry_after = int(self.window - (now - oldest)) + 1
            return False, retry_after
        timestamps.append(now)
        return True, 0

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        now = time.time()
        if now % 10 < 0.5:
            self._cleanup(self.uuid_requests)
            self._cleanup(self.ip_requests)

        uuid = request.headers.get("x-user-id")
        client_ip = self._get_client_ip(request)

        if uuid:
            allowed, retry_after = self._check_limit(
                uuid, self.uuid_requests, self.uuid_limit
            )
            if not allowed:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "UUID rate limit exceeded"},
                    headers={"Retry-After": str(retry_after)},
                )

        allowed, retry_after = self._check_limit(
            client_ip, self.ip_requests, self.ip_limit
        )
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "IP rate limit exceeded"},
                headers={"Retry-After": str(retry_after)},
            )

        return await call_next(request)
