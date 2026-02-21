from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password, hash_password
from app.core.config import settings
from app.schemas.auth import Token

router = APIRouter()

# En un proyecto real esto vendría de la DB.
# Para el pipeline de CI usamos un usuario hardcodeado en settings.
FAKE_USERS_DB = {
    settings.ADMIN_USERNAME: {
        "username": settings.ADMIN_USERNAME,
        "hashed_password": hash_password(settings.ADMIN_PASSWORD),
    }
}


@router.post("/token", response_model=Token, summary="Obtener token JWT")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Recibe username y password, devuelve un JWT access token.
    Usar el token en el header: Authorization: Bearer <token>
    """
    user = FAKE_USERS_DB.get(form_data.username)

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": user["username"]})
    return Token(access_token=token)
