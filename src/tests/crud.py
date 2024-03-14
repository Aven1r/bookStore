import pytest_asyncio

from src.models import sellers
from src.models.sellers import Seller
from src.tests.examples import ORIGINAL_SELLER_1_HASHED, ORIGINAL_SELLER_2_HASHED
from src.models import books
from src.models.books import Book
from src.models.sellers import Seller
from src.tests.models import BookExample


@pytest_asyncio.fixture()
async def get_new_seller(db_session) -> Seller:
    seller = sellers.Seller(**ORIGINAL_SELLER_1_HASHED)
    db_session.add(seller)
    await db_session.flush()
    yield seller


@pytest_asyncio.fixture()
async def get_2_new_sellers(db_session) -> Seller:
    seller_1 = sellers.Seller(**ORIGINAL_SELLER_1_HASHED)
    seller_2 = sellers.Seller(**ORIGINAL_SELLER_2_HASHED)
    db_session.add_all([seller_1, seller_2])
    await db_session.flush()
    yield seller_1, seller_2


async def add_book_for_seller(db_session, sellerID):
    book = books.Book(**BookExample(seller_id=sellerID).to_dict())
    db_session.add(book)
    await db_session.flush()
    return book


async def add_2_books_for_seller(db_session, sellerID):
    book_1 = books.Book(**BookExample(seller_id=sellerID).to_dict())
    book_2 = books.Book(**BookExample(seller_id=sellerID).to_dict())
    db_session.add_all([book_1, book_2])
    await db_session.flush()
    return book_1, book_2
