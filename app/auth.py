from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import TOKEN_STORE
import time

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    current_token = TOKEN_STORE.get("token")
    expiry = TOKEN_STORE.get("expires_at")

    if not current_token or not expiry:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not initialized or missing",
        )

    if time.time() >= expiry:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    if credentials.scheme != "Bearer" or credentials.credentials != current_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
