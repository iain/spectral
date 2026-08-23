"""Exponential backoff with jitter, because the network is not your friend."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field

MAX_ATTEMPTS = 5
BASE_DELAY = 0.25


@dataclass(slots=True)
class RetryPolicy:
    attempts: int = MAX_ATTEMPTS
    base: float = BASE_DELAY
    retry_on: tuple[type[Exception], ...] = (TimeoutError, ConnectionError)
    _clock: callable = field(default=time.monotonic, repr=False)

    def delay_for(self, attempt: int) -> float:
        """Full-jitter backoff: uniform over [0, base * 2**attempt]."""
        if attempt < 0:
            raise ValueError(f"attempt must be non-negative, got {attempt!r}")
        return random.uniform(0.0, self.base * (2 ** attempt))

    def call(self, fn, *args, **kwargs):
        last = None
        for attempt in range(self.attempts):
            try:
                return fn(*args, **kwargs)
            except self.retry_on as exc:
                last = exc
                time.sleep(self.delay_for(attempt))
        raise RuntimeError("retries exhausted") from last
