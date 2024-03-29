import json
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.models.books import Book
from src.schemas import IncomingBook, ReturnedAllBooks, ReturnedBook, UpdateBook
from src.schemas import SellerOut
from src.db.crud.auth import get_current_seller

books_router = APIRouter(tags=["books"], prefix="/books")

# Больше не симулируем хранилище данных. Подключаемся к реальному, через сессию.
DBSession = Annotated[AsyncSession, Depends(get_async_session)]


# Ручка для создания записи о книге в БД. Возвращает созданную книгу.
@books_router.post("/", response_model=ReturnedBook, status_code=status.HTTP_201_CREATED)  # Прописываем модель ответа
async def create_book(
    book: IncomingBook, session: DBSession, current_seller: SellerOut = Depends(get_current_seller)
):  # прописываем модель валидирующую входные данные и сессию как зависимость.
    # это - бизнес логика. Обрабатываем данные, сохраняем, преобразуем и т.д.
    new_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        count_pages=book.count_pages,
        seller_id=current_seller.id
    )
    session.add(new_book)
    await session.flush()

    return new_book


# Ручка, возвращающая все книги
@books_router.get("/", response_model=ReturnedAllBooks)
async def get_all_books(session: DBSession):
    query = select(Book)
    res = await session.execute(query)
    books = res.scalars().all()
    return {"books": books}


# Ручка для получения книги по ее ИД
@books_router.get("/{book_id}", response_model=ReturnedBook)
async def get_book(book_id: int, session: DBSession):
    res = await session.get(Book, book_id)
    return res


# Ручка для удаления книги
@books_router.delete("/{book_id}")
async def delete_book(book_id: int, session: DBSession):
    deleted_book = await session.get(Book, book_id)
    if deleted_book:
        await session.delete(deleted_book)

    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Response может вернуть текст и метаданные.


# Ручка для обновления данных о книге
@books_router.put("/{book_id}", status_code=status.HTTP_200_OK, response_model=ReturnedBook)
async def update_book(book_id: int, new_data: UpdateBook, session: DBSession, current_seller: SellerOut = Depends(get_current_seller)):
    if updated_book := await session.get(Book, book_id):
        updated_book.author = new_data.author
        updated_book.title = new_data.title
        updated_book.year = new_data.year
        updated_book.count_pages = new_data.count_pages
        updated_book.seller_id = new_data.seller_id

        await session.flush()

        return updated_book

    return Response(status_code=status.HTTP_404_NOT_FOUND)
