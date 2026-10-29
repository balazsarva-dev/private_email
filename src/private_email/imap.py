from imaplib import IMAP4_SSL
from private_email.models import Message
from private_email.config import HOST, USER, PASSWORD, IMAP_PORT
from email import policy
import email
from typing import List

def connect():
    host, user, password, port = HOST, USER, PASSWORD, IMAP_PORT
    auth = IMAP4_SSL(host, port)
    auth.login(user, password)
    return auth

def fetch_messages(folder: str) -> List[Message]:
    get_connect = connect()
    get_connect.select(folder)
    _, data = get_connect.uid("search", None, "ALL")
    uids = data[0].split()
    messages = []
    for uid in uids:
        _, data = get_connect.uid("fetch", uid, "(RFC822)")
        messages.append(parse_message(uid, data[0][1]))
    get_connect.logout()
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
    get_connect = connect()
    get_connect.select(folder)
    _, data = get_connect.uid("search", None, "ALL")
    uids = data[0].split()
    count = len(uids)
    for uid in uids:
        get_connect.uid("store", uid, "+FLAGS", r"(\Deleted)")
    get_connect.expunge()
    get_connect.logout()
    return count

def delete(message_id: int, folder: str) -> bool:
    get_connect = connect()
    get_connect.select(folder)
    uid = str(message_id)
    _, data = get_connect.uid("search", None, "UID", uid)
    if not data[0]:
        get_connect.logout()
        return False
    get_connect.uid("store", uid, "+FLAGS", r"(\Deleted)")
    get_connect.expunge()
    get_connect.logout()
    return True
