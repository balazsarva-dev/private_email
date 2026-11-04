from imaplib import IMAP4_SSL
from private_email.models import Message
from private_email.config import HOST, USER, PASSWORD, IMAP_PORT
from email import policy
import email
from typing import List
from contextlib import contextmanager

# This function creates a connection to the email server.
def connect():
    make_connection = IMAP4_SSL(HOST, IMAP_PORT)
    make_connection.login(USER, PASSWORD)
    return make_connection

# This function creates a context manager for a mailbox.
@contextmanager
def mailbox(folder: str):
    imap = connect()
    imap.select(folder)
    try:
        yield imap
    finally:
        imap.logout()

# This function fetches all messages from a mailbox.
def fetch_messages(folder: str) -> List[Message]:
    with mailbox(folder) as imap:
        _, data = imap.uid("search", None, "ALL")
        uids = data[0].split()
        messages = []
        for uid in uids:
            _, data = imap.uid("fetch", uid, "(RFC822)")
            parsed_message = parse_message(uid, data[0][1])
            messages.append(parsed_message)
    return messages

# This function parses a message from a raw email.
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

# This function vacuums a mailbox.
def vacuum(folder: str) -> int:
    with mailbox(folder) as imap:
        _, data = imap.uid("search", None, "ALL")
        uids = data[0].split()
        count = len(uids)
        for uid in uids:
            imap.uid("store", uid, "+FLAGS", r"(\Deleted)")
        imap.expunge()
        return count

# This function deletes a message from a mailbox.
def delete(message_id: int, folder: str) -> bool:
    with mailbox(folder) as imap:
        uid = str(message_id)
        _, data = imap.uid("search", None, "UID", uid)
        if not data[0]:
            return False
        imap.uid("store", uid, "+FLAGS", r"(\Deleted)")
        imap.expunge()
        return True
