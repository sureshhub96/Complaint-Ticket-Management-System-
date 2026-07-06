from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(
        ...,
        pattern=r"^[0-9]{10}$"
    )
    address: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^[0-9]{10}$"
    )
    address: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int
    created_by: int

    class Config:
        from_attributes = True