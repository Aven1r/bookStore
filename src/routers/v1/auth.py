from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas import Token
from src.configurations.settings import settings
from src.auth.jwt import create_access_token
from src.db.crud.auth import authenticate_seller

from src.db.utils import DBSession

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def seller_login(session: DBSession, form_data: OAuth2PasswordRequestForm = Depends()):
    seller = await authenticate_seller(session, form_data.username, form_data.password)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(seller.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}