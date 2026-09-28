import json
import logging
from typing import Any

logger = logging.getLogger("restaurant_agent")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def log_event(event: str, **data: Any) -> None:
    logger.info(json.dumps({"event": event, **data}, default=str))
