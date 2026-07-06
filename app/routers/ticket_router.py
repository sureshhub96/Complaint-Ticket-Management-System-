from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.oauth2 import get_current_user
from app.core.dependencies import admin_required

from app.schemas.ticket import TicketCreate, TicketUpdate

from app.services.ticket_service import (
    create_ticket,
    get_all_tickets,
    get_ticket,
    update_ticket,
    delete_ticket,
    assign_ticket,
    get_customer_tickets,
    get_agent_tickets,
    search_tickets,
    filter_by_priority,
    filter_by_status,
    filter_tickets,
    get_tickets_paginated,
    ticket_dashboard,
    agent_workload
)

router = APIRouter()


# ======================================================
# Create Ticket
# ======================================================
@router.post("/")
def add_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_ticket(ticket, current_user, db)


# ======================================================
# Get All Tickets
# ======================================================
@router.get("/")
def tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_all_tickets(db)


# ======================================================
# Search Tickets
# ======================================================
@router.get("/search")
def search(
    title: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return search_tickets(title, db)


# ======================================================
# Filter Tickets
# ======================================================
@router.get("/filter")
def filter_ticket(
    priority: str | None = None,
    status_value: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if priority and status_value:
        return filter_tickets(priority, status_value, db)

    if priority:
        return filter_by_priority(priority, db)

    if status_value:
        return filter_by_status(status_value, db)

    return {
        "message": "Please provide priority or status_value."
    }


# ======================================================
# Pagination
# ======================================================
@router.get("/pagination")
def pagination(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_tickets_paginated(page, limit, db)


# ======================================================
# Dashboard Report (Admin Only)
# ======================================================
@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return ticket_dashboard(db)


# ======================================================
# Get Tickets of Customer
# ======================================================
@router.get("/customer/{customer_id}")
def customer_tickets(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_customer_tickets(customer_id, current_user, db)


# ======================================================
# Get Tickets Assigned to Agent
# ======================================================
@router.get("/agent/{agent_id}")
def agent_tickets(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_agent_tickets(agent_id, current_user, db)


# ======================================================
# Agent Workload (Admin Only)
# ======================================================
@router.get("/workload/{agent_id}")
def workload(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return agent_workload(agent_id, db)


# ======================================================
# Get Ticket By ID
# ======================================================
@router.get("/{ticket_id}")
def ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_ticket(ticket_id, db)


# ======================================================
# Update Ticket
# ======================================================
@router.put("/{ticket_id}")
def edit_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_ticket(
        ticket_id,
        ticket,
        current_user,
        db
    )


# ======================================================
# Delete Ticket (Admin Only)
# ======================================================
@router.delete("/{ticket_id}")
def remove_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return delete_ticket(ticket_id, db)


# ======================================================
# Assign Ticket to Support Agent (Admin Only)
# ======================================================
@router.post("/{ticket_id}/assign/{agent_id}")
def assign(
    ticket_id: int,
    agent_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return assign_ticket(
        ticket_id,
        agent_id,
        db
    )
