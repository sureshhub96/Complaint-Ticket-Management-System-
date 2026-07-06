from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import Base, engine

# Import models so SQLAlchemy registers them
from app.models.user import User
from app.models.customer import Customer
from app.models.ticket import Ticket

# Routers
from app.routers.auth_router import router as auth_router
from app.routers.customer_router import router as customer_router
from app.routers.ticket_router import router as ticket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create database tables when the application starts.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Complaint & Ticket Management System",
    description="Complaint & Ticket Management REST API using FastAPI",
    version="1.0.0",
    lifespan=lifespan,
)


# ==========================
# Root Endpoint
# ==========================
@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Complaint & Ticket Management System API",
        "version": "1.0.0",
        "status": "Running"
    }


# ==========================
# Health Check
# ==========================
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "OK",
        "database": "Connected"
    }


# ==========================
# Include Routers
# ==========================
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    customer_router,
    prefix="/customers",
    tags=["Customers"]
)

app.include_router(
    ticket_router,
    prefix="/tickets",
    tags=["Tickets"]
)