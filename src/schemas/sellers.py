from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from src.schemas.books import ReturnedBook

__all__ = ["Seller", "SellerAuth", "SellerOut", "AllSellers", "SellerBooks"]


class Seller(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class SellerAuth(Seller):
    password: str


class SellerOut(Seller):
    id: int

    class Config:
        orm_mode = True


class AllSellers(BaseModel):
    sellers: List[SellerOut]



class SellerBooks(SellerOut):
    books: Optional[List[ReturnedBook]] = []

    class Config:
        from_attributes = True
