from imaplib import IMAP4_SSL
from private_email.models import Message
from private_email.config import HOST, USER, PASSWORD, IMAP_PORT
from email import policy
import email
from typing import List
from contextlib import contextmanager

def connect():
    host, user, password, port = HOST, USER, PASSWORD, IMAP_PORT
    auth = IMAP4_SSL(host, port)
    auth.login(user, password)
    return auth

@contextmanager
def mailbox(folder: str):
    imap = connect()
    imap.select(folder)
    try:
        yield imap
    finally:
        imap.logout()

def fetch_messages(folder: str) -> List[Message]:
    with mailbox(folder) as imap:
        _, data = imap.uid("search", None, "ALL")
        uids = data[0].split()
        messages = []
        for uid in uids:
            _, data = imap.uid("fetch", uid, "(RFC822)")
            messages.append(parse_message(uid, data[0][1]))
    return messages

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

def vacuum(folder: str) -> int:
    with mailbox(folder) as imap:
        _, data = imap.uid("search", None, "ALL")
        uids = data[0].split()
        count = len(uids)
        for uid in uids:
            imap.uid("store", uid, "+FLAGS", r"(\Deleted)")
        imap.expunge()
        return count

def delete(message_id: int, folder: str) -> bool:
    with mailbox(folder) as imap:
        uid = str(message_id)
        _, data = imap.uid("search", None, "UID", uid)
        if not data[0]:
            return False
        imap.uid("store", uid, "+FLAGS", r"(\Deleted)")
        imap.expunge()
        return True
