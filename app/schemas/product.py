from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Request schemas ──────────────────────────────────────
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Laptop Pro")
    description: Optional[str] = Field(None, max_length=500, example="Laptop de alto rendimiento")
    price: float = Field(..., gt=0, example=999.99)
    stock: int = Field(default=0, ge=0, example=50)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


# ── Response schemas ─────────────────────────────────────
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Permite convertir modelos SQLAlchemy a Pydantic


# ── Paginación ───────────────────────────────────────────
class PaginatedProducts(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[ProductResponse]
