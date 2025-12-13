from rich import print
from src.job_executor import JobExecutor
from src.mail_context import MailContext
from src.db_connectors.sqlite_connector import sqlite_db
from src.models import MailSQLite 
import threading
import asyncio

class MailHandler:
    async def handle_DATA(self, server, session, envelope):
        print(f"[blue]Received on thread: {threading.get_ident()}[/blue]")
        print("Message from:", envelope.mail_from)
        print("Message to:", envelope.rcpt_tos)
        asyncio.create_task(MailHandler.process_email(envelope))
        print("250 OK - Email is being processed asynchronously.")
        return '250 OK'
    
    @staticmethod
    async def process_email(envelope):
        print("Processing email asynchronously...")
        mail_context = MailContext.from_envelope(envelope)
        mail_data = MailSQLite.from_context(mail_context)
        mail_data = await sqlite_db.save_email(mail_data)
        results = await JobExecutor(mail_context).execute_jobs()
        mail_data.append_job_results(results)
        await sqlite_db.update_email(mail_data)
        print("Mail Data:", mail_data.to_dict())