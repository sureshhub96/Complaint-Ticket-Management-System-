from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(String(30), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    assigned_tickets = relationship(
        "Ticket",
        back_populates="agent",
        foreign_keys="Ticket.assigned_agent_id"
    )