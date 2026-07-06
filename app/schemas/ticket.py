from pydantic import BaseModel
from typing import Optional


class TicketBase(BaseModel):
    customer_id: int
    title: str
    description: str
    priority: str
    category: str


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None


class TicketResponse(BaseModel):
    id: int
    customer_id: int
    title: str
    description: str
    priority: str
    category: str
    status: str
    assigned_agent_id: Optional[int] = None

    class Config:
        from_attributes = True