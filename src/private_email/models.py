from pydantic import BaseModel, Field

class Message(BaseModel):
    message_id : int = Field(description="Message identification number")
    sender : str = Field(description="Message sender")
    receiver : str = Field(description="Message receiver")
    subject : str = Field(description="Message subject")
    date : str = Field(description="Message date (Date header)")
    content : str = Field(description="Message content")
