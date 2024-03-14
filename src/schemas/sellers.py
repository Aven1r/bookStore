from typing import List

from pydantic import BaseModel, EmailStr

from src.schemas.books import ReturnedBook

__all__ = ["Seller", "SellerAuth", "SellerOut", "AllSellers", "ReturnedSellerBooks"]


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


class ReturnedSellerBooks(SellerOut):
    books: list[ReturnedBook]
