import os
import time
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from imaplib import Time2Internaldate
from smtplib import SMTP_SSL
from private_email.imap import connect


def send(receiver: str, subject: str, content: str, html: str | None = None) -> None:
    host = os.getenv("PRIVATEEMAIL_HOST", "")
    user = os.getenv("PRIVATEEMAIL_USER", "")
    password = os.getenv("PRIVATEEMAIL_PASSWORD", "")

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = receiver
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=user.split("@")[-1])
    msg.set_content(content)
    if html:
        msg.add_alternative(html, subtype="html")

    with SMTP_SSL(host, 465) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)

    # Save a copy to "Sent", otherwise the follow-up skill can't find it.
    imap = connect()
    imap.append("Sent", r"(\Seen)", Time2Internaldate(time.time()), msg.as_bytes())
    imap.logout()
