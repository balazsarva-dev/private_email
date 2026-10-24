from imaplib import IMAP4_SSL
import os
from private_email.models import Message
import email
from email import policy


def connect():
    host = os.getenv("PRIVATEEMAIL_HOST", "")
    user = os.getenv("PRIVATEEMAIL_USER", "")
    password = os.getenv("PRIVATEEMAIL_PASSWORD", "")
    auth = IMAP4_SSL(host, 993)
    auth.login(user, password)
    return auth

def parse_message(uid: bytes, raw: bytes) -> Message:
    msg = email.message_from_bytes(raw, policy=policy.default)
    body = msg.get_body(preferencelist=("plain", "html"))
    content = body.get_content() if body is not None else ""
    return Message(
                    message_id=int(uid),
                    sender=msg.get("From", ""),
                    receiver=msg.get("To", ""),
                    subject=msg.get("Subject", ""),
                    date=msg.get("Date", ""),
                    content=content
    )
