from typing import Any, List
from mcp.server.mcpserver import MCPServer
from imaplib import IMAP4
from pydantic import BaseModel

mcp = MCPServer[Any] ("private_email")

class Message(BaseModel):
    message_id : int
    sender : str
    receiver : str
    subject : str
    content : str

def fetch_messages(folder: str) -> List[Message]:
    return [
        Message(message_id=1, sender="Rob", receiver="Kate", 
                subject="Welcome message", content="Hello Kate, I hope you are doing fine"),
        Message(message_id=2, sender="Kate", receiver="Rob", 
                subject="Welcome message", content="Hello Rob, Yes, I am fine."),
        Message(message_id=3, sender="Rob", receiver="Kate",
                subject="Response", content="Great."),
    ]

@mcp.tool()
def list_messages(folder: str = "INBOX", limit: int = 10) -> List[Message]:
    messages = fetch_messages(folder)
    result = []
    for message in messages[:limit]:
        result.append(message)
    return result

@mcp.tool()
def read_message(message_id: int, folder: str = "INBOX") -> str:
    messages = fetch_messages(folder)
    for message in messages:
        if message.message_id == message_id:
            return message.content
    return "No message found."

@mcp.tool()
def search_message(query: str, folder: str = "INBOX") -> List[Message]:
    messages = fetch_messages(folder)
    result = []
    for message in messages:
        if query in message.content:
            result.append(message)
    return result

@mcp.tool()
def delete_message(message_id: int, folder: str = "INBOX"):
    messages = fetch_messages(folder)
    for message in messages:
        if message.message_id == message_id:
            messages.remove(message)

@mcp.tool()
def send_message(receiver:str, subject: str, content: str):
    msg = Message(receiver=receiver, subject=subject, content=content)


if __name__ == "__main__":
    mcp.run()

