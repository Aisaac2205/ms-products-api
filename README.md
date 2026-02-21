# ms-products-api 🛒

Microservicio REST de gestión de productos construido con **FastAPI**, **PostgreSQL** y autenticación **JWT**.

![CI](https://github.com/Aisaac2205/ms-products-api/actions/workflows/ci.yml/badge.svg)

## Stack

- **Python 3.11** + **FastAPI** — framework web async
- **PostgreSQL** — base de datos relacional
- **SQLAlchemy** — ORM para Python
- **JWT** (JSON Web Tokens) — autenticación stateless
- **Pydantic v2** — validación de datos
- **Docker** — containerización

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/auth/token` | ❌ | Obtener JWT |
| POST | `/products/` | ✅ | Crear producto |
| GET | `/products/` | ✅ | Listar productos (paginado) |
| GET | `/products/{id}` | ✅ | Obtener producto |
| PATCH | `/products/{id}` | ✅ | Actualizar producto |
| DELETE | `/products/{id}` | ✅ | Eliminar producto (soft delete) |
| GET | `/health` | ❌ | Health check |

## Setup local

```bash
# 1. Clonar el repo
git clone https://github.com/Aisaac2205/ms-products-api.git
cd ms-products-api

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 5. Levantar PostgreSQL (necesitas Docker)
docker run -d \
  --name products-db \
  -e POSTGRES_USER=testuser \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=productsdb \
  -p 5432:5432 \
  postgres:15

# 6. Correr la API
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`
Documentación interactiva: `http://localhost:8000/docs`

## Tests E2E

Los tests viven en el repo [ms-products-tests](https://github.com/Aisaac2205/ms-products-tests).
Se ejecutan automáticamente cuando se hace push a `main` o `develop`.

## Estructura del proyecto

```
ms-products-api/
├── app/
│   ├── main.py           # Entry point
│   ├── core/
│   │   ├── config.py     # Variables de entorno
│   │   └── security.py   # JWT utilities
│   ├── db/
│   │   └── database.py   # Conexión SQLAlchemy
│   ├── models/
│   │   └── product.py    # Modelo de DB
│   ├── schemas/
│   │   ├── product.py    # Schemas Pydantic
│   │   └── auth.py
│   └── routers/
│       ├── products.py   # CRUD endpoints
│       └── auth.py       # Login endpoint
├── Dockerfile
├── requirements.txt
└── .github/
    └── workflows/
        └── ci.yml        # Pipeline CI
```
