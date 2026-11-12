import time
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from imaplib import Time2Internaldate
from smtplib import SMTP_SSL
from private_email.imap import connect
from private_email.config import HOST, USER, PASSWORD, SMTP_PORT


def create_email(receiver: str, subject: str, content: str, html: str | None = None) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = USER
    msg["To"] = receiver
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=USER.split("@")[-1])
    msg.set_content(content)
    if html:
        msg.add_alternative(html, subtype="html")
    return msg


def send(receiver: str, subject: str, content: str, html: str | None = None) -> bool:
    msg = create_email(receiver, subject, content, html)
    with SMTP_SSL(HOST, SMTP_PORT) as smtp:
        smtp.login(USER, PASSWORD)
        smtp.send_message(msg)
    # Save a copy to "Sent", otherwise the follow-up skill can't find it.
    try:
        save_copy("Sent", r"(\Seen)", msg)
        return True
    except Exception:
        return False

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
