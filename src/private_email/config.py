import os
from dotenv import load_dotenv

load_dotenv()

def _require(name: str) -> str:
    env_variable = os.getenv(name)
    if not env_variable:
        raise RuntimeError(f"Missing environment variable: {name}")
    return env_variable

HOST = _require("PRIVATEEMAIL_HOST")
IMAP_PORT = int(_require("IMAP_PORT"))
SMTP_PORT = int(_require("SMTP_PORT"))
USER = _require("PRIVATEEMAIL_USER")
PASSWORD = _require("PRIVATEEMAIL_PASSWORD")
