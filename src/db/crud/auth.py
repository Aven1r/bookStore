from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.auth.security import verify_password
from src.db.crud.seller import get_seller_by_email
from src.db.utils import DBSession
from src.auth.jwt import decode_access_token
from src.db.crud.seller import get_seller_by_id
from src.auth.jwt import credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_seller(session: DBSession, email: str, password: str):
    seller = await get_seller_by_email(session, email)
    if not seller:
        return False
    if not verify_password(password, seller.hashed_password):
        return False
    return seller

async def get_current_seller(session: DBSession, token: str = Depends(oauth2_scheme)):
    token_data = decode_access_token(token)
    seller = await get_seller_by_id(session, token_data.id)
    if seller is None:
        raise credentials_exception
    return seller