from attr import dataclass

@dataclass
class MailData():
    sender: str
    recipient: str
    subject: str
    body: str
    job_results: dict
    raw_email: str