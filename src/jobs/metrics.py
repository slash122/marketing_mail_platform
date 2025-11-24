import asyncio
from unittest import result
from src.jobs.base_job import Job
from lxml import etree
from src.utils import parse_email_body

class EmailMetricsJob(Job):
    def __init__(self, envelope):
        self.envelope = envelope
        self.raw_email = envelope.content.decode('unicode_escape', errors='replace')
        self.email_body = parse_email_body(envelope)
        self.email_etree = etree.fromstring(self.email_body, parser=etree.HTMLParser())
        self.email_text = etree.tostring(self.email_etree, method='text', encoding='unicode')   

    async def run(self):
        result = {}
        result['word_count'] = len(self.email_text.split())
        result['char_count'] = len(self.email_text)
        result['line_count'] = len(self.email_text.splitlines())
        result['paragraph_count'] = len(self.email_text.split('\n\n'))
        result['sentence_count'] = self.email_text.count('.') + self.email_text.count('!') + self.email_text.count('?')
        result['average_word_length'] = self.average_word_length(result)
        result['reading_time_seconds'] = (result['word_count'] / 200) * 60 
        return result

    def average_word_length(self, result) -> float:
        if result['word_count'] == 0: return 0
        return sum(len(word) for word in self.email_text.split()) / result['word_count']