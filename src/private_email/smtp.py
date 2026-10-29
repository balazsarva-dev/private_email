import time
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from imaplib import Time2Internaldate
from smtplib import SMTP_SSL
from private_email.imap import connect
from private_email.config import HOST, USER, PASSWORD, SMTP_PORT

def send(receiver: str, subject: str, content: str, html: str | None = None) -> None:
    host, user, password, port = HOST, USER, PASSWORD, SMTP_PORT

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = receiver
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=user.split("@")[-1])
    msg.set_content(content)
    if html:
        msg.add_alternative(html, subtype="html")

    with SMTP_SSL(host, port) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)

    # Save a copy to "Sent", otherwise the follow-up skill can't find it.
    imap = connect()
    imap.append("Sent", r"(\Seen)", Time2Internaldate(time.time()), msg.as_bytes())
    imap.logout()


def draft(receiver: str, subject: str, content: str, html: str | None = None) -> None:
    user = USER

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = receiver
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=user.split("@")[-1])
    msg.set_content(content)
    if html:
        msg.add_alternative(html, subtype="html")

    # No SMTP here, the draft only goes to "Drafts" so it can be reviewed and sent from webmail.
    imap = connect()
    imap.append("Drafts", r"(\Draft)", Time2Internaldate(time.time()), msg.as_bytes())
    imap.logout()
