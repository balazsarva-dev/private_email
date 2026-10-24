from typing import Any, List
from mcp.server.mcpserver import MCPServer
from dotenv import load_dotenv
from private_email.models import Message
from private_email.imap import connect, parse_message

mcp = MCPServer[Any] ("private_email")


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

@mcp.tool()
def list_messages(folder: str = "INBOX", limit: int = 10) -> List[Message]:
    """
    List the most recent messages in a folder (default: INBOX), newest first,
    at most `limit` of them. Use this for an overview, e.g. when the user asks
    'list my emails', 'what did I get recently' or 'summarize my emails'.
    """
    messages = fetch_messages(folder)
    result = []
    for message in messages[::-1][:limit]:
        result.append(message)
    return result

@mcp.tool()
def read_message(message_id: int, folder: str = "INBOX") -> str:
    """
    Return the full text of one specific message by its ID. Use this after
    list_messages or search_message, when the user wants to read a given email.
    """
    messages = fetch_messages(folder)
    for message in messages:
        if message.message_id == message_id:
            return message.content
    return "No message found."

@mcp.tool()
def search_message(query: str, folder: str = "INBOX") -> List[Message]:
    """
    Find messages whose subject or text contains `query` (case-insensitive).
    Use this when the user looks for an email about something specific.
    """
    messages = fetch_messages(folder)
    result = []
    for message in messages:
        if query.lower() in message.subject.lower() or query.lower() in message.content.lower():
            result.append(message)
    return result

def delete_message(message_id: int, folder: str = "INBOX"):
    messages = fetch_messages(folder)
    for message in messages:
        if message.message_id == message_id:
            messages.remove(message)

def send_message(receiver:str, subject: str, content: str):
    pass

def main():
    load_dotenv()
    mcp.run()
