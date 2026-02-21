from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, auth
from app.db.database import engine, Base

# Crear todas las tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ms-products-api",
    description="Microservicio de productos con autenticación JWT",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de salud — usado por el pipeline CI para saber que el servidor está listo."""
    return {"status": "ok", "service": "ms-products-api"}
