from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.complaints import router as complaints_router
from app.services import database_service

app = FastAPI(title="Auth API", version="0.1.0")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5175",
    "http://localhost:5176",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(complaints_router, prefix="/api/v1")


@app.on_event("startup")
def startup_event() -> None:
    """Initializes the database schema on startup."""
    database_service.init_db()


@app.get("/")
def read_root():
    """Health check endpoint to verify API status."""
    return {"message": "API is running"}
