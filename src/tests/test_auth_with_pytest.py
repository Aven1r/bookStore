import pytest
from fastapi import status

from src.tests.examples import API_PREFIX, ORIGINAL_SELLER_1_PASSWORD
from src.tests.crud import get_new_seller, get_2_new_sellers


@pytest.mark.asyncio
async def test_login_success(async_client, db_session, get_new_seller):
    seller = get_new_seller

    login_data = {"username": seller.email, 
                  "password": ORIGINAL_SELLER_1_PASSWORD}

    response = await async_client.post(API_PREFIX + "token", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(async_client, db_session, get_new_seller):
    seller = get_new_seller

    login_data = {"username": seller.email, "password": ORIGINAL_SELLER_1_PASSWORD + "fdfdfdff"}

    response = await async_client.post(API_PREFIX + "token", data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_wrong_email(async_client, db_session, get_new_seller):
    seller = get_new_seller

    login_data = {"username": seller.email + "fdfdfdfdf", "password": ORIGINAL_SELLER_1_PASSWORD}

    response = await async_client.post(API_PREFIX + "token", data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED