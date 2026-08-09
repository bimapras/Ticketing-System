from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
    
class CreateTicket(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=5, max_length=1000)
    priority: Literal['low', 'medium', 'high'] = 'low'
    created_by: Optional[str] = Field(max_length=50)
    
    @field_validator("created_by", mode="before")
    @classmethod
    def empty_to_default(cls, value):
        if value in (None, ""):
            return "Anonymous"
        return value
    
class UpdateTicketStatus(BaseModel):
    status: Literal['open', 'in_progress', 'resolved']
    
class ReplyTicketMessage(BaseModel):
    ticket_id: int
    author: str = Field(max_length=50)
    message_text: Optional[str] = Field(min_length=5, max_length=1000)
    status: UpdateTicketStatus
    
    @field_validator("author", mode="before")
    @classmethod
    def empty_to_default(cls, value):
        if value in (None, ""):
            return "Admin"
        return value
