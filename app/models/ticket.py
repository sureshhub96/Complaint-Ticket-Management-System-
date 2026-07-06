from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    priority = Column(
        String(20),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    status = Column(
        String(30),
        default="Open"
    )

    assigned_agent_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    customer = relationship(
        "Customer",
        back_populates="tickets"
    )

    agent = relationship(
        "User",
        back_populates="assigned_tickets",
        foreign_keys=[assigned_agent_id]
    )