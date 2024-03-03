from fastapi import APIRouter, Depends, status

from src.schemas import SellerOut, Seller, SellerAuth, AllSellers, SellerBooks
from src.db.crud.seller import add_new_seller, get_sellers_crud, delete_seller_crud, update_seller_crud, get_seller_crud
from src.db.crud.auth import get_current_seller
# from src.utils.auth import check_seller_token
from src.db.utils import DBSession

sellers_router = APIRouter(tags=["sellers"], prefix="/seller")


@sellers_router.post("/", response_model=Seller, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: SellerAuth, session: DBSession):
    return await add_new_seller(seller, session)


@sellers_router.get("/", response_model=AllSellers)
async def get_all_sellers(session: DBSession):
    return await get_sellers_crud(session)


@sellers_router.delete("/{seller_id}")
async def delete_seller(seller_id: int, session: DBSession):
    return await delete_seller_crud(seller_id, session)


@sellers_router.put("/{seller_id}", response_model=Seller)
async def update_seller(seller_id: int, new_data: Seller, session: DBSession):
    return await update_seller_crud(seller_id, new_data, session)


@sellers_router.get("/{seller_id}", response_model=SellerBooks)
async def get_seller(seller_id: int, session: DBSession, current_seller: Seller = Depends(get_current_seller)):
    return await get_seller_crud(seller_id, session)