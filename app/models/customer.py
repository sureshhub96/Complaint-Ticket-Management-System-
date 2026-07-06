from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    phone = Column(String(15), unique=True, nullable=False)

    address = Column(String(255), nullable=False)

    # Relationship
    tickets = relationship(
        "Ticket",
        back_populates="customer",
        cascade="all, delete"
    )