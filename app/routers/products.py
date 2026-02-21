from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, PaginatedProducts
from app.core.security import decode_token

router = APIRouter()


# ── CREATE ───────────────────────────────────────────────
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: str = Depends(decode_token),  # Requiere JWT
):
    """Crea un nuevo producto. Requiere autenticación."""
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# ── READ ALL (con paginación) ────────────────────────────
@router.get("/", response_model=PaginatedProducts)
def list_products(
    page: int = Query(default=1, ge=1, description="Número de página"),
    page_size: int = Query(default=10, ge=1, le=100, description="Items por página"),
    db: Session = Depends(get_db),
    _: str = Depends(decode_token),
):
    """Lista todos los productos activos con paginación."""
    query = db.query(Product).filter(Product.is_active == True)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedProducts(
        total=total,
        page=page,
        page_size=page_size,
        items=items,
    )


# ── READ ONE ─────────────────────────────────────────────
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(decode_token),
):
    """Obtiene un producto por su ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


# ── UPDATE ───────────────────────────────────────────────
@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(decode_token),
):
    """Actualiza parcialmente un producto. Requiere autenticación."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    update_data = payload.model_dump(exclude_unset=True)  # Solo los campos enviados
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


# ── DELETE (soft delete) ─────────────────────────────────
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(decode_token),
):
    """
    Elimina un producto (soft delete — solo lo marca como inactivo).
    Buena práctica: nunca borrar datos reales en producción.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    product.is_active = False
    db.commit()
