from rich import print
from src.job_executor import JobExecutor
from src.mail_data import MailData
from src.utils import prepare_envelope
import threading
import time

class MailHandler:
    async def handle_DATA(self, server, session, envelope):
        print(f"[blue]Received on thread: {threading.get_ident()}[/blue]")
        print("Message from:", envelope.mail_from)
        print("Message to:", envelope.rcpt_tos)
        await MailHandler.process_email(envelope)
        return '250 OK'
    
    @staticmethod
    async def process_email(envelope):
        print("Processing email asynchronously...")
        time_received = int(time.time())
        email_raw_data = prepare_envelope(envelope)
        results = await JobExecutor(email_raw_data).execute_jobs()
        mail_data = MailData.create_mail_data(time_received, envelope, email_raw_data, results)
        print("Mail Data:", mail_data.to_dict())
    