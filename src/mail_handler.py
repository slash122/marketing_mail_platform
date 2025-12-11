from rich import print
from src.job_launcher import JobLauncher
from src.mail_data import MailData
from src.utils import prepare_envelope
import threading

class MailHandler:
    async def handle_DATA(self, server, session, envelope):
        print(f"[blue]Received on thread: {threading.get_ident()}[/blue]")
        print("Message from:", envelope.mail_from)
        print("Message to:", envelope.rcpt_tos)
        await MailHandler.process_email(envelope)
        return '250 OK'
    
    async def process_email(envelope):
        print("Processing email asynchronously...")
        email_raw_data = prepare_envelope(envelope)
        job_launcher = JobLauncher(email_raw_data)
        results = await job_launcher.launch_jobs()
        print(results)
        print("Email processed.")

    async def prepare_mail_data(self, envelope, email_raw_data, job_results):
        mail_data = MailData(
            sender = envelope.mail_from,
            recipient = ', '.join(envelope.rcpt_tos),
            subject = email_raw_data['etree'].xpath('//title/text()')[0] if email_raw_data['etree'].xpath('//title/text()') else 'No Subject',
            body = email_raw_data['text'],
            job_results = job_results,
            raw_email = email_raw_data['raw_email']
        )