from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.config import settings
from app.models.counsellor import Counsellor
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_counsellor(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        counsellor_id: str = payload.get("sub")
        if counsellor_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    try:
        # Verify it's a valid UUID
        parsed_id = uuid.UUID(counsellor_id)
    except ValueError:
        raise credentials_exception
        
    result = await db.execute(select(Counsellor).where(Counsellor.id == parsed_id))
    counsellor = result.scalars().first()
    
    if counsellor is None:
        raise credentials_exception
        
    if not counsellor.is_active:
        raise HTTPException(status_code=403, detail="Inactive counsellor")
        
    return counsellor
