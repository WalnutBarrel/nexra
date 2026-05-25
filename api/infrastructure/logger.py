import json
import uuid
from datetime import datetime

class StructuredLogger:
    """Produces JSON-structured, searchable operational logs."""
    
    def __init__(self, subsystem: str):
        self.subsystem = subsystem

    def _log(self, level: str, message: str, **kwargs):
        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "subsystem": self.subsystem,
            "message": message,
            "trace_id": kwargs.pop("trace_id", str(uuid.uuid4())),
        }
        payload.update(kwargs)
        # In production, this goes to stdout for Datadog/ELK parsing
        # print(json.dumps(payload))

    def info(self, message: str, **kwargs):
        self._log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log("WARN", message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log("ERROR", message, **kwargs)

    def fatal(self, message: str, **kwargs):
        self._log("FATAL", message, **kwargs)

def get_logger(subsystem: str) -> StructuredLogger:
    return StructuredLogger(subsystem)
