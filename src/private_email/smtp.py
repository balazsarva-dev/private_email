import time
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from imaplib import Time2Internaldate
from smtplib import SMTP_SSL
from private_email.imap import connect, fetch_original
from private_email.config import HOST, USER, PASSWORD, SMTP_PORT


def create_email(
    receiver: str, 
    subject: str,
    content: str, 
    html: str | None = None,
    in_reply_to: str | None = None,
    references: str | None = None
) -> EmailMessage:

    msg = EmailMessage()
    msg["From"] = USER
    msg["To"] = receiver
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=USER.split("@")[-1])
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = references
    msg.set_content(content)
    if html:
        msg.add_alternative(html, subtype="html")
    return msg


def send(receiver: str, subject: str, content: str, html: str | None = None) -> bool:
    msg = create_email(receiver, subject, content, html)
    return deliver(msg)

def deliver(msg: EmailMessage) -> bool:
    with SMTP_SSL(HOST, SMTP_PORT) as smtp:
        smtp.login(USER, PASSWORD)
        smtp.send_message(msg)
    # Save a copy to "Sent", otherwise the follow-up skill can't find it.
    try:
        save_copy("Sent", r"(\Seen)", msg)
        return True
    except Exception:
        return False

def reply(message_id: int, folder: str, content: str, html: str | None = None) -> bool:
    original_message = fetch_original(message_id, folder)
    if original_message is None:
        raise ValueError("No original message found.")
    receiver = original_message.get("Reply-To", "") or original_message.get("From", "")
    subject = original_message.get("Subject", "")
    if not subject.lower().startswith("re:"):
        subject = "Re: " + subject
    in_reply_to = original_message.get("Message-ID")
    references = (original_message.get("References", "") + " " + in_reply_to).strip()

    msg = create_email(receiver, subject, content, html, in_reply_to, references)
    return deliver(msg)

def save_copy(folder: str, flag: str, msg: EmailMessage) -> None:
    imap = connect()
    try:
        status, _ = imap.append(folder, flag, Time2Internaldate(time.time()), msg.as_bytes())
        if status != "OK":
            raise ValueError(f"Could not save to folder: {folder}")
    finally:
        imap.logout()


def draft(receiver: str, subject: str, content: str, html: str | None = None) -> None:
    msg = create_email(receiver, subject, content, html)
    # No SMTP here, the draft only goes to "Drafts" so it can be reviewed and sent from webmail.
    save_copy("Drafts", r"(\Draft)", msg)
