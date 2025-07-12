# src/utils/monitoring.py
import time
import logging
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class PipelineMonitor:
    def __init__(self):
        self.start_time = None
        self.stages = {}
        self.success_count = 0
        self.total_requests = 0

    def start_pipeline(self):
        self.start_time = time.time()
        self.total_requests += 1
        logger.info("Pipeline started")

    def log_stage(self, stage_name, input_data=None, output_data=None, error=None):
        elapsed = time.time() - self.start_time
        self.stages[stage_name] = {
            "latency": elapsed,
            "input": input_data,
            "output": output_data,
            "error": str(error) if error else None
        }
        if error:
            logger.error(f"Stage {stage_name} failed: {str(error)}")
        else:
            logger.info(f"Stage {stage_name} completed in {elapsed:.2f}s: {output_data}")
            if stage_name == "tts":
                self.success_count += 1

    def get_metrics(self):
        success_rate = (self.success_count / self.total_requests * 100) if self.total_requests > 0 else 0
        return {
            "stages": self.stages,
            "success_rate": success_rate,
            "total_requests": self.total_requests,
            "total_latency": time.time() - self.start_time if self.start_time else 0
        }

    def log_metrics(self):
        metrics = self.get_metrics()
        logger.info(f"Pipeline metrics: Success rate={metrics['success_rate']:.2f}%, "
                   f"Total requests={metrics['total_requests']}, "
                   f"Total latency={metrics['total_latency']:.2f}s")

monitor = PipelineMonitor()
