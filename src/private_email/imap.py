from imaplib import IMAP4_SSL
from private_email.models import Message
from private_email.config import HOST, USER, PASSWORD, IMAP_PORT
from email import policy
import email


def connect():
    host, user, password, port = HOST, USER, PASSWORD, IMAP_PORT
    auth = IMAP4_SSL(host, port)
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
