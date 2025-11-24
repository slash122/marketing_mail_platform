from rich import print
from src.jobs.metrics import EmailMetricsJob

import threading

class MailHandler:
    async def handle_DATA(self, server, session, envelope):
        print(f"[blue]Received on thread: {threading.get_ident()}[/blue]")
        print("Message from:", envelope.mail_from)
        print("Message to:", envelope.rcpt_tos)
        # print("Content:\n", envelope.content.decode('unicode_escape', errors='replace'))
        await MailHandler.process_email(envelope)
        return '250 OK'
    
    async def process_email(envelope):
        # Placeholder for asynchronous email processing logic
        print("Processing email asynchronously...")
        metrics_job = EmailMetricsJob(envelope)
        metrics = await metrics_job.run()
        print(metrics)
        print("Email processed.")
        