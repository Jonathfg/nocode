from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.db.database import get_session
from app.auth.utils import decode_token
from app.crud.user import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)):
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        role: str = payload.get("role")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

def require_role(*allowed_roles):
    def checker(user=Depends(get_current_user)):
        if user.role.value not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permiso denegado")
        return user
    return checker