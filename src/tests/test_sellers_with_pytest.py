import pytest
from fastapi import status
from sqlalchemy import select, delete
from datetime import timedelta

from src.models import books, sellers
from src.configurations.settings import settings
from src.auth.jwt import create_access_token
from src.tests.examples import (
    ORIGINAL_SELLER_1_HASHED,
    NEW_SELLER_1,
    API_PREFIX,
    ORIGINAL_SELLER_1,
    ORIGINAL_SELLER_1_PASSWORD,
)

from src.tests.crud import get_2_new_sellers, get_new_seller, add_2_books_for_seller


@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = ORIGINAL_SELLER_1
    response = await async_client.post(API_PREFIX + "seller/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == {
        "first_name": ORIGINAL_SELLER_1_HASHED["first_name"],
        "last_name": ORIGINAL_SELLER_1_HASHED["last_name"],
        "email": ORIGINAL_SELLER_1_HASHED["email"],
    }


@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client, get_2_new_sellers):
    seller_1, seller_2 = get_2_new_sellers

    response = await async_client.get(API_PREFIX + "seller/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2

    assert response.json() == {
        "sellers": [
            {
                "first_name": seller_1.first_name,
                "last_name": seller_1.last_name,
                "email": seller_1.email,
                "id": seller_1.id,
            },
            {
                "first_name": seller_2.first_name,
                "last_name": seller_2.last_name,
                "email": seller_2.email,
                "id": seller_2.id,
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_single_seller_without_books(db_session, async_client, get_2_new_sellers):
    # Подготовка: создание пользователя для аутентификации
    seller_1, seller_2 = get_2_new_sellers

    # Аутентификация пользователя для получения токена
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(seller_1.id)}, expires_delta=access_token_expires
    )

    # Выполнение запроса по 2-ому продавцу с токеном аутентификации
    response = await async_client.get(
        API_PREFIX + f"seller/{seller_2.id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_200_OK

    # Проверка интерфейса ответа
    assert response.json() == {
        "first_name": seller_2.first_name,
        "last_name": seller_2.last_name,
        "email": seller_2.email,
        "id": seller_2.id,
        "books": [],
    }


@pytest.mark.asyncio
async def test_get_single_seller_with_books(db_session, async_client, get_2_new_sellers):

    seller_1, seller_2 = get_2_new_sellers

    # Аутентификация пользователя для получения токена
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(seller_1.id)}, expires_delta=access_token_expires
    )

    book_1, book_2 = await add_2_books_for_seller(db_session=db_session, sellerID=seller_2.id)

    # Выполнение запроса по 2-ому продавцу с токеном аутентификации
    response = await async_client.get(
        API_PREFIX + f"seller/{seller_2.id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_200_OK

    # Проверка ожидаемого интерфейса ответа
    expected_books = [
        {
            "title": book_1.title,
            "author": book_1.author,
            "year": book_1.year,
            "id": book_1.id,
            "count_pages": book_1.count_pages,
            "seller_id": book_1.seller_id,
        },
        {
            "title": book_2.title,
            "author": book_2.author,
            "year": book_2.year,
            "id": book_2.id,
            "count_pages": book_2.count_pages,
            "seller_id": book_2.seller_id,
        },
    ]

    assert response.json() == {
        "first_name": seller_2.first_name,
        "last_name": seller_2.last_name,
        "email": seller_2.email,
        "id": seller_2.id,
        "books": expected_books,
    }


@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client, get_new_seller):
    seller = get_new_seller

    response = await async_client.delete(API_PREFIX + f"seller/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.Seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0


@pytest.mark.asyncio
async def test_delete_seller_with_books(db_session, async_client, get_new_seller):
    seller = get_new_seller

    book_1, book_2 = await add_2_books_for_seller(db_session=db_session, sellerID=seller.id)

    # Delete books associated with the seller before deleting the seller
    await db_session.execute(delete(books.Book).where(books.Book.seller_id == seller.id))
    await db_session.flush()

    response = await async_client.delete(API_PREFIX + f"seller/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.Seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0

    res = await db_session.execute(select(books.Book).where(books.Book.id == book_1.id))
    book = res.scalars().first()
    assert book is None

    res = await db_session.execute(select(books.Book).where(books.Book.id == book_2.id))
    book = res.scalars().first()
    assert book is None


@pytest.mark.asyncio
async def test_update_seller(db_session, async_client, get_new_seller):
    seller = get_new_seller

    response = await async_client.put(
        API_PREFIX + f"seller/{seller.id}",
        json={
            "first_name": NEW_SELLER_1["first_name"],
            "last_name": NEW_SELLER_1["last_name"],
            "email": NEW_SELLER_1["email"],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(sellers.Seller, seller.id)
    assert res.first_name == NEW_SELLER_1["first_name"]
    assert res.last_name == NEW_SELLER_1["last_name"]
    assert res.email == NEW_SELLER_1["email"]
