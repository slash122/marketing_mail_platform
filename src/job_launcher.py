from src.jobs.ai_personalization import AiPersonalizationJob
from src.jobs.metrics import MetricsJob
from src.jobs.ai_spam_check import AiSpamCheckJob
from src.jobs.ai_summary import AiSummaryJob
from src.utils import prepare_envelope
import asyncio
import importlib
import inspect
from pathlib import Path

class JobLauncher:
    def __init__(self, email_data):
        self.email_data = email_data
        self.jobs = self.get_jobs()

    def get_jobs(self):
        jobs_dir = Path(__file__).parent / 'jobs'
        job_classes = []

        for file in jobs_dir.glob('*.py'):
            if file.name.startswith('_'):
                continue
            module_name = f'src.jobs.{file.stem}'
            module = importlib.import_module(module_name)
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name.endswith('Job') and obj.__module__ == module_name:
                    job_classes.append(obj)
        
        return [job_class(self.email_data) for job_class in job_classes]

    async def launch_jobs(self):
        results = await asyncio.gather(*(job.execute() for job in self.jobs))
        return results