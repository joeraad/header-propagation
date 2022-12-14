from contextvars import ContextVar
from typing import Optional

# Middleware
propagated_headers: ContextVar[Optional[str]] = ContextVar('propagated_headers', default={})
