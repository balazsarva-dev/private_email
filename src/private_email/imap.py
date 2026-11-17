from imaplib import IMAP4_SSL
from private_email.models import Message
from private_email.config import HOST, USER, PASSWORD, IMAP_PORT
from email import policy
from email.message import EmailMessage
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
    try:
        status, _ = imap.select(folder)
        if status != "OK":
            raise ValueError(f"Folder not found: {folder}")
        yield imap
    finally:
        imap.logout()

# This function fetches all messages from a mailbox.
def fetch_messages(folder: str, limit: int | None = None) -> List[Message]:
    with mailbox(folder) as imap:
        uids = all_uids(imap)
        messages = []
        if limit:
            uids = uids[-limit:]
        for uid in uids:
            _, data = imap.uid("fetch", uid, "(BODY.PEEK[])")
            parsed_message = parse_message(uid, data[0][1])
            messages.append(parsed_message)
    return messages


def all_uids(imap) -> List[bytes]:
    _, data = imap.uid("search", None, "ALL")
    uids = data[0].split()
    return uids


def fetch_message(message_id: int, folder: str) -> Message | None:
    with mailbox(folder) as imap:
        uid = str(message_id)
        _, data = imap.uid("fetch", uid, "(BODY.PEEK[])")
        if not data or data[0] is None:
            return None
        return parse_message(uid.encode(), data[0][1])


def fetch_original(message_id: int, folder: str) -> EmailMessage | None:
    with mailbox(folder) as imap:
        uid = str(message_id)
        _, data = imap.uid("fetch", uid, "(BODY.PEEK[])")
        if not data or data[0] is None:
            return None
        return email.message_from_bytes(data[0][1], policy=policy.default)


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
        uids = all_uids(imap)
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
        imap.uid("expunge", uid)
        return True
