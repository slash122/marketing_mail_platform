from pydantic import BaseModel

class MailData(BaseModel):
    surrogate_key: str = None
    time_received: int
    sender: str
    recipient: str
    subject: str
    body: str
    job_results: dict
    raw_email: str
    errors: list
    
    def to_dict(self):
        return self.model_dump()
    
    @classmethod
    def create_mail_data(cls, time_received, envelope, email_raw_data, job_results):
        prepared_results, errors = MailData._prepare_job_results(job_results)
        return MailData(
            time_received = time_received,
            sender = envelope.mail_from,
            recipient = ', '.join(envelope.rcpt_tos),
            subject = email_raw_data['subject'],
            body = email_raw_data['text'],
            job_results = prepared_results,  
            raw_email = email_raw_data['raw_email'],
            errors = errors
        )

    @staticmethod
    def _prepare_job_results(raw_job_results):
        prepared_results = {}
        errors = []
        for result_pair in raw_job_results:
            if 'exception' in result_pair:
                errors.append(result_pair)
            else:
                prepared_results[result_pair['job_name']] = result_pair['result']
        return prepared_results, errors