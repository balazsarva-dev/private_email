from imaplib import IMAP4_SSL
import os
from private_email.models import Message

def connect():
    host = os.getenv("PRIVATEEMAIL_HOST", "")
    user = os.getenv("PRIVATEEMAIL_USER", "")
    password = os.getenv("PRIVATEEMAIL_PASSWORD", "")
    auth = IMAP4_SSL(host, 993)
    auth.login(user, password)
    return auth

def parse_message(uid: bytes, raw: bytes) -> Message:
    pass