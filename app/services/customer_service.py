from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


# =====================================================
# Create Customer
# =====================================================
def create_customer(
    customer: CustomerCreate,
    current_user,
    db: Session
):
    # Check email
    existing_email = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer email already exists"
        )

    # Check phone
    existing_phone = db.query(Customer).filter(
        Customer.phone == customer.phone
    ).first()

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already exists"
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        created_by=current_user.id
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {
        "message": "Customer created successfully",
        "customer": new_customer
    }


# =====================================================
# Get All Customers
# =====================================================
def get_all_customers(db: Session):

    customers = db.query(Customer).all()

    return customers


# =====================================================
# Get Customer By ID
# =====================================================
def get_customer(
    customer_id: int,
    db: Session
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return customer


# =====================================================
# Update Customer
# =====================================================
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session
):

    db_customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    if customer.name is not None:
        db_customer.name = customer.name

    if customer.email is not None:

        existing_email = db.query(Customer).filter(
            Customer.email == customer.email,
            Customer.id != customer_id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        db_customer.email = customer.email

    if customer.phone is not None:

        existing_phone = db.query(Customer).filter(
            Customer.phone == customer.phone,
            Customer.id != customer_id
        ).first()

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already exists"
            )

        db_customer.phone = customer.phone

    if customer.address is not None:
        db_customer.address = customer.address

    db.commit()
    db.refresh(db_customer)

    return {
        "message": "Customer updated successfully",
        "customer": db_customer
    }


# =====================================================
# Delete Customer
# =====================================================
def delete_customer(
    customer_id: int,
    db: Session
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }


# =====================================================
# Search Customers
# =====================================================
def search_customers(
    name: str,
    db: Session
):

    customers = db.query(Customer).filter(
        Customer.name.ilike(f"%{name}%")
    ).all()

    return customers


# =====================================================
# Get Customers With Pagination
# =====================================================
def get_customers_paginated(
    page: int,
    limit: int,
    db: Session
):

    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    offset = (page - 1) * limit

    customers = (
        db.query(Customer)
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(Customer).count()

    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_records": total,
        "total_pages": total_pages,
        "customers": customers
    }