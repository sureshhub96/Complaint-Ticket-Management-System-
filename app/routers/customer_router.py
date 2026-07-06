from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.oauth2 import get_current_user
from app.core.dependencies import admin_required

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate
)

from app.services.customer_service import (
    create_customer,
    get_all_customers,
    get_customer,
    update_customer,
    delete_customer,
    search_customers,
    get_customers_paginated
)

router = APIRouter()


# ==========================================
# Create Customer
# ==========================================
@router.post("/")
def add_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_customer(customer, current_user, db)


# ==========================================
# Get All Customers
# ==========================================
@router.get("/")
def customers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_all_customers(db)


# ==========================================
# Pagination
# ==========================================
@router.get("/page")
def customer_pagination(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_customers_paginated(page, limit, db)


# ==========================================
# Search Customer
# ==========================================
@router.get("/search")
def search_customer(
    name: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return search_customers(name, db)


# ==========================================
# Get Customer By ID
# ==========================================
@router.get("/{customer_id}")
def customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_customer(customer_id, db)


# ==========================================
# Update Customer
# ==========================================
@router.put("/{customer_id}")
def edit_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_customer(customer_id, customer, db)


# ==========================================
# Delete Customer
# Admin Only
# ==========================================
@router.delete("/{customer_id}")
def remove_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return delete_customer(customer_id, db)