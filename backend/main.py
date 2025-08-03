import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.entity_router import generate_entity_router
from backend.utils.config import get_client_name

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Read client name from .env or config
client_name = get_client_name()

# ✅ Register single dynamic entity router
app.include_router(
    generate_entity_router(client_name),
    prefix="/api",
    tags=["Entity"]
)
