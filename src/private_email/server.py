from typing import Any, List
from mcp.server.mcpserver import MCPServer
from private_email.models import Message
from private_email.imap import connect, parse_message
from private_email.smtp import send, draft

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
    Find messages whose sender, receiver, subject or text contains `query`
    (case-insensitive), newest first. Use this when the user looks for an email
    about something specific, or for emails to/from a given address
    (e.g. folder "Sent" with the receiver's email address).
    """
    messages = fetch_messages(folder)
    result = []
    for message in messages[::-1]:
        fields = (message.sender, message.receiver, message.subject, message.content)
        if any(query.lower() in field.lower() for field in fields):
            result.append(message)
    return result

@mcp.tool()
def delete_message(message_id: int, folder: str = "INBOX") -> str:
    """
    Permanently delete one specific message by its ID (from list_messages or search_message).
    Use this when the user wants to delete a given email. Ask permission before deleting,
    this cannot be undone.
    """
    get_connect = connect()
    get_connect.select(folder)
    uid = str(message_id)
    _, data = get_connect.uid("search", None, "UID", uid)
    if not data[0]:
        get_connect.logout()
        return "No message found."
    get_connect.uid("store", uid, "+FLAGS", r"(\Deleted)")
    get_connect.expunge()
    get_connect.logout()
    return f"Message {message_id} deleted from {folder}."

@mcp.tool()
def vacuum_folder(folder: str = "Trash") -> str:
    """
    Permanently delete all messages in a folder (default: Trash). Use this when the user
    wants to empty / vacuum the Trash. Ask permission before deleting, this cannot be undone.
    INBOX, Sent and Drafts are protected and cannot be emptied.
    """
    if folder.lower() in ("inbox", "sent", "drafts"):
        return f"The {folder} folder is protected, nothing was deleted."
    get_connect = connect()
    get_connect.select(folder)
    _, data = get_connect.uid("search", None, "ALL")
    uids = data[0].split()
    for uid in uids:
        get_connect.uid("store", uid, "+FLAGS", r"(\Deleted)")
    get_connect.expunge()
    get_connect.logout()
    return f"{len(uids)} messages deleted from {folder}."

@mcp.tool()
def send_message(receiver:str, subject: str, content: str, html: str | None = None) -> str:
    """
    This function is for sending message to a specific receiver. Use this when the user
    wants to send a message to someone with a subject and some content. Ask permission before sending.
    `content` is the plain-text body. Pass `html` as well to send an HTML version
    (e.g. with a formatted signature); `content` is then the fallback for clients without HTML.
    """
    send(receiver=receiver, subject=subject, content=content, html=html)
    return f"Message sent successfully to {receiver}!"

@mcp.tool()
def draft_message(receiver:str, subject: str, content: str, html: str | None = None) -> str:
    """
    This function saves a message to the "Drafts" folder without sending it. Use this when the user
    wants a draft, or wants to review an email in webmail before sending it.
    `content` is the plain-text body. Pass `html` as well to save an HTML version
    (e.g. with a formatted signature); `content` is then the fallback for clients without HTML.
    """
    draft(receiver=receiver, subject=subject, content=content, html=html)
    return f"Draft for {receiver} saved to Drafts!"

def main():
    mcp.run()
