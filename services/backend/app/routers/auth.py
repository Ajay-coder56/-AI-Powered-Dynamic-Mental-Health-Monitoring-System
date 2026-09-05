from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.auth import Token
from app.schemas.counsellor import CounsellorResponse
from app.database import get_db
from app.models.counsellor import Counsellor
from app.security import verify_password, create_access_token
from app.dependencies import get_current_counsellor

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # form_data.username will contain the email
    result = await db.execute(select(Counsellor).where(Counsellor.email == form_data.username))
    counsellor = result.scalars().first()
    
    if not counsellor or not verify_password(form_data.password, counsellor.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not counsellor.is_active:
        raise HTTPException(status_code=403, detail="Inactive counsellor")
        
    access_token = create_access_token(subject=str(counsellor.id))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=CounsellorResponse)
async def get_me(current_counsellor: Counsellor = Depends(get_current_counsellor)):
    return current_counsellor
