from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
from app.db.database import get_session
from app.crud.user import (
    create_user,
    get_user_by_username,
    get_user_by_email,
)
from app.auth import utils
from app.auth.schemas import (
    UserCreate,
    LoginData,
    Token,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordReset,
)
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Lista en memoria de tokens revocados
REVOKED_TOKENS = set()

def _create_tokens_for_user(user):
    access = utils.create_access_token(sub=user.username, role=user.role.value)
    refresh = utils.create_refresh_token(sub=user.username, role=user.role.value)
    expires = utils.ACCESS_TOKEN_EXPIRE[user.role.value] * 60
    return Token(
        access_token=access,
        refresh_token=refresh,
        expires_in=expires
    )

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, session: Session = Depends(get_session)):
    if get_user_by_username(session, data.username) or get_user_by_email(session, data.email):
        raise HTTPException(status_code=400, detail="Usuario o email ya existe")
    user = create_user(
        session,
        username=data.username,
        email=data.email,
        password=data.password,
        role=data.role
    )
    if not user:
        raise HTTPException(status_code=400, detail="Error al crear usuario")
    return _create_tokens_for_user(user)

@router.post("/login", response_model=Token)
def login(data: LoginData, session: Session = Depends(get_session)):
    user = get_user_by_username(session, data.username)
    if not user or not utils.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return _create_tokens_for_user(user)

@router.post("/refresh", response_model=Token)
def refresh(tokens: RefreshTokenRequest):
    try:
        payload = utils.decode_token(tokens.refresh_token)
        if tokens.refresh_token in REVOKED_TOKENS:
            raise HTTPException(status_code=401, detail="Refresh token revocado")
        username = payload["sub"]
        role = payload["role"]
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido")
    access = utils.create_access_token(sub=username, role=role)
    refresh = utils.create_refresh_token(sub=username, role=role)
    expires = utils.ACCESS_TOKEN_EXPIRE[role] * 60
    return Token(access_token=access, refresh_token=refresh, expires_in=expires)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(token: str = Depends(oauth2_scheme)):
    REVOKED_TOKENS.add(token)
    return

@router.post("/forgot-password")
def forgot_password(req: PasswordResetRequest, session: Session = Depends(get_session)):
    user = get_user_by_email(session, req.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email no registrado")
    reset_token = utils.create_password_reset_token(user.email)
    return {"reset_token": reset_token}

@router.post("/reset-password")
def reset_password(data: PasswordReset, session: Session = Depends(get_session)):
    try:
        payload = utils.decode_token(data.token)
        email = payload["sub"]
    except Exception:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    user = get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.hashed_password = utils.get_password_hash(data.new_password)
    session.add(user)
    session.commit()
    return {"msg": "Contraseña actualizada"}