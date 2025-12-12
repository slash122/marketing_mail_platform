import asyncio
from src.base_job import EmailJob
from src.utils import perform_ai_request

class AiSummaryJob(EmailJob):
    async def run(self):
        prompt = f"Summarize the following email content in a concise manner:\n\n{self.text}"
        return await perform_ai_request(prompt)
    
    async def mock_run(self):
        await asyncio.sleep(0.1)
        return "This is a mock summary of the email content."