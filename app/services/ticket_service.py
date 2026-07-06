from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.ticket import Ticket
from app.models.customer import Customer
from app.models.user import User

from app.schemas.ticket import TicketCreate, TicketUpdate


# ==========================================================
# Create Ticket
# ==========================================================

def create_ticket(
    ticket: TicketCreate,
    current_user,
    db: Session
):

    customer = db.query(Customer).filter(
        Customer.id == ticket.customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # Customer users can create tickets only for customers they created.
    if (
        current_user.role == "Customer"
        and customer.created_by != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to create tickets for this customer."
        )

    new_ticket = Ticket(
        customer_id=ticket.customer_id,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        category=ticket.category,
        status="Open"
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket created successfully",
        "ticket": new_ticket
    }


# ==========================================================
# Get All Tickets
# ==========================================================

def get_all_tickets(db: Session):

    tickets = db.query(Ticket).all()

    return tickets


# ==========================================================
# Get Ticket By ID
# ==========================================================

def get_ticket(ticket_id: int, db: Session):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket


# ==========================================================
# Get Tickets of a Customer
# ==========================================================

def get_customer_tickets(
    customer_id: int,
    current_user,
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

    if (
        current_user.role == "Customer"
        and customer.created_by != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    tickets = db.query(Ticket).filter(
        Ticket.customer_id == customer_id
    ).all()

    return tickets


# ==========================================================
# Get Tickets Assigned to an Agent
# ==========================================================

def get_agent_tickets(
    agent_id: int,
    current_user,
    db: Session
):

    if (
        current_user.role == "Support Agent"
        and current_user.id != agent_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your assigned tickets."
        )

    agent = db.query(User).filter(
        User.id == agent_id,
        User.role == "Support Agent"
    ).first()

    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support agent not found"
        )

    tickets = db.query(Ticket).filter(
        Ticket.assigned_agent_id == agent_id
    ).all()

    return tickets

# ==========================================================
# Update Ticket
# ==========================================================

def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    current_user,
    db: Session
):

    db_ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if db_ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    # Closed tickets cannot be updated
    if db_ticket.status == "Closed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Closed tickets cannot be updated"
        )

    # ----------------------------
    # Customer Permission
    # ----------------------------
    if current_user.role == "Customer":

        customer = db.query(Customer).filter(
            Customer.id == db_ticket.customer_id
        ).first()

        if customer.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        # Customer cannot change status
        if ticket.status is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Customers cannot change ticket status"
            )

    # ----------------------------
    # Support Agent Permission
    # ----------------------------
    if current_user.role == "Support Agent":

        if db_ticket.assigned_agent_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only assigned support agent can update this ticket"
            )

    # ----------------------------
    # Update Fields
    # ----------------------------

    if ticket.title is not None:
        db_ticket.title = ticket.title

    if ticket.description is not None:
        db_ticket.description = ticket.description

    if ticket.priority is not None:
        db_ticket.priority = ticket.priority

    if ticket.category is not None:
        db_ticket.category = ticket.category

    # Only Admin or Assigned Agent
    if ticket.status is not None:

        if current_user.role == "Admin":
            db_ticket.status = ticket.status

        elif (
            current_user.role == "Support Agent"
            and db_ticket.assigned_agent_id == current_user.id
        ):
            db_ticket.status = ticket.status

    db.commit()
    db.refresh(db_ticket)

    return {
        "message": "Ticket updated successfully",
        "ticket": db_ticket
    }


# ==========================================================
# Delete Ticket
# ==========================================================

def delete_ticket(
    ticket_id: int,
    db: Session
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted successfully"
    }


# ==========================================================
# Assign Ticket to Support Agent
# ==========================================================

def assign_ticket(
    ticket_id: int,
    agent_id: int,
    db: Session
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if ticket.assigned_agent_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket is already assigned"
        )

    agent = db.query(User).filter(
        User.id == agent_id,
        User.role == "Support Agent"
    ).first()

    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support Agent not found"
        )

    ticket.assigned_agent_id = agent_id

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket assigned successfully",
        "ticket": ticket
    }

from sqlalchemy import or_

# ==========================================================
# Search Tickets By Title
# ==========================================================

def search_tickets(
    title: str,
    db: Session
):

    tickets = db.query(Ticket).filter(
        Ticket.title.ilike(f"%{title}%")
    ).all()

    return tickets


# ==========================================================
# Filter By Priority
# ==========================================================

def filter_by_priority(
    priority: str,
    db: Session
):

    tickets = db.query(Ticket).filter(
        Ticket.priority == priority
    ).all()

    return tickets


# ==========================================================
# Filter By Status
# ==========================================================

def filter_by_status(
    status_value: str,
    db: Session
):

    tickets = db.query(Ticket).filter(
        Ticket.status == status_value
    ).all()

    return tickets


# ==========================================================
# Filter By Priority & Status
# ==========================================================

def filter_tickets(
    priority: str = None,
    status_value: str = None,
    db: Session = None
):

    query = db.query(Ticket)

    if priority:
        query = query.filter(
            Ticket.priority == priority
        )

    if status_value:
        query = query.filter(
            Ticket.status == status_value
        )

    return query.all()


# ==========================================================
# Pagination
# ==========================================================

def get_tickets_paginated(
    page: int,
    limit: int,
    db: Session
):

    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    offset = (page - 1) * limit

    tickets = (
        db.query(Ticket)
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(Ticket).count()

    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_records": total,
        "total_pages": total_pages,
        "tickets": tickets
    }


# ==========================================================
# Dashboard Report
# ==========================================================

def ticket_dashboard(db: Session):

    total = db.query(Ticket).count()

    open_count = db.query(Ticket).filter(
        Ticket.status == "Open"
    ).count()

    progress_count = db.query(Ticket).filter(
        Ticket.status == "In Progress"
    ).count()

    resolved_count = db.query(Ticket).filter(
        Ticket.status == "Resolved"
    ).count()

    closed_count = db.query(Ticket).filter(
        Ticket.status == "Closed"
    ).count()

    return {
        "total_tickets": total,
        "open": open_count,
        "in_progress": progress_count,
        "resolved": resolved_count,
        "closed": closed_count
    }


# ==========================================================
# Agent Workload
# ==========================================================

def agent_workload(
    agent_id: int,
    db: Session
):

    agent = db.query(User).filter(
        User.id == agent_id,
        User.role == "Support Agent"
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Support Agent not found"
        )

    tickets = db.query(Ticket).filter(
        Ticket.assigned_agent_id == agent_id
    ).all()

    return {
        "agent_id": agent.id,
        "agent_name": agent.username,
        "assigned_tickets": len(tickets),
        "tickets": tickets
    }
    