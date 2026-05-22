from app.core.logger import log_event
from app.core.config import get_config_value
from datetime import datetime


class ExecutionController:
    def __init__(self):
        self.status = "idle"
        self.retry_limit = get_config_value("execution.retry_limit", 0)

    def execute(self, task_name: str, handler):
        self.status = "running"
        log_event("ExecutionController", "execute_start", "RUNNING", task_name)
        
        start_time = datetime.utcnow()

        retry_count = 0
        while True:
            try:
                result = handler()
                end_time = datetime.utcnow()
                duration = (end_time - start_time).total_seconds()
                self.status = "success"
                log_event("ExecutionController", "execute_success", "SUCCESS", f"{task_name} - Duration: {duration:.2f}s")
                return result
            except Exception as error:
                retry_count += 1
                if retry_count <= self.retry_limit:
                    log_event("ExecutionController", "execute_retry", "RETRY", f"Attempt {retry_count}: {str(error)}")
                    continue
                else:
                    end_time = datetime.utcnow()
                    duration = (end_time - start_time).total_seconds()
                    self.status = "failed"
                    log_event("ExecutionController", "execute_failed", "FAILED", f"{str(error)} - Duration: {duration:.2f}s")
                    raise