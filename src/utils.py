from email import message_from_bytes
from typing import Dict, List, Optional

def parse_email_body(envelope) -> Dict:
    msg = message_from_bytes(envelope.content)
    return msg.get_payload(decode=True).decode('utf-8', errors='replace')