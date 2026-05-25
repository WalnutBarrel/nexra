import uuid
from typing import Callable, Any, Dict

class RedisQueue:
    """Mock RQ (Redis Queue) for background job processing."""
    
    def __init__(self):
        self.active_jobs = []
        self.queued_jobs = []
        self.dead_letter = []
        self.processed = 0

    def enqueue(self, func: Callable, *args, **kwargs) -> str:
        job_id = str(uuid.uuid4())
        self.queued_jobs.append({
            "id": job_id,
            "func": func.__name__,
            "status": "queued"
        })
        return job_id

    def simulate_processing(self):
        # Move from queued to processed
        for job in self.queued_jobs:
            self.processed += 1
        self.queued_jobs = []

    def simulate_failure(self, job_name: str, error: str):
        self.dead_letter.append({
            "id": str(uuid.uuid4()),
            "func": job_name,
            "error": error
        })

    def get_telemetry(self) -> Dict[str, Any]:
        return {
            "active_workers": 4,
            "queue_depth": len(self.queued_jobs),
            "dead_letter_count": len(self.dead_letter),
            "total_processed": self.processed
        }

rq_client = RedisQueue()
