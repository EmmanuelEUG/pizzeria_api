from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import catalogo, carritos, tickets

app = FastAPI(
    title="Pizzería Chevery API",
    description="API RESTful para el flujo de pedidos de Pizzería Chevery (Suchiapa, Chiapas)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar al puerto de tu frontend en producción
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(catalogo.router)
app.include_router(carritos.router)
app.include_router(tickets.router)