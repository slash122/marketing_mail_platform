from attr import dataclass
from pydantic import BaseModel

class MailData(BaseModel):
    surrogate_key: str = None
    time_received: str
    sender: str
    recipient: str
    subject: str
    body: str
    job_results: dict
    raw_email: str
    any_errors: bool
    
    def to_dict(self):
        return self.model_dump()
    
    @classmethod
    def create_mail_data(cls, time_received, envelope, email_raw_data, job_results):
        return MailData(
            time_received = time_received,
            sender = envelope.mail_from,
            recipient = ', '.join(envelope.rcpt_tos),
            subject = email_raw_data['subject'],
            body = email_raw_data['text'],
            job_results = job_results,  
            raw_email = email_raw_data['raw_email'],
            any_errors = MailData._results_contain_errors(job_results)
        )

    @staticmethod
    def _results_contain_errors(job_results):
        for result in job_results:
            if 'exception' in result:
                return True
        return False