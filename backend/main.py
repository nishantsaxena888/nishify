from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.entity_router import generate_entity_router
from backend.utils.config import get_client_name

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client_name = get_client_name()

app.include_router(
    generate_entity_router(client_name),
    prefix="/api",
    tags=["Entity"]
)
