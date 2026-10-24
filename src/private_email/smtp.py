import os
from email.message import EmailMessage
from smtplib import SMTP_SSL


def send(receiver: str, subject: str, content: str, html: str | None = None) -> None:
    host = os.getenv("PRIVATEEMAIL_HOST", "")
    user = os.getenv("PRIVATEEMAIL_USER", "")
    password = os.getenv("PRIVATEEMAIL_PASSWORD", "")

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(content)
    if html:
        msg.add_alternative(html, subtype="html")

    with SMTP_SSL(host, 465) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)
