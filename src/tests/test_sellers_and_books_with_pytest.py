import pytest
from fastapi import status

from src.tests.examples import ORIGINAL_SELLER_1, API_PREFIX, ORIGINAL_SELLER_1_PASSWORD, NEW_SELLER_1
from src.tests.crud import get_new_seller, get_2_new_sellers


from .models import BookExample


@pytest.mark.asyncio
async def test_create_addbook_update_delete_seller(async_client, db_session, get_new_seller):
    seller = get_new_seller

    login_data = {"username": seller.email,
                  "password": ORIGINAL_SELLER_1_PASSWORD}

    response = await async_client.post(API_PREFIX + "token", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    access_token = response.json()["access_token"]

    # Seller info

    response = await async_client.get(
        API_PREFIX + f"seller/{seller.id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_200_OK

    book = BookExample(seller_id=seller.id).to_dict()

    # Book creation

    response = await async_client.post(
        API_PREFIX + "books/", headers={"Authorization": f"Bearer {access_token}"}, json=book
    )

    assert response.status_code == status.HTTP_201_CREATED

    # Seller info

    response = await async_client.get(
        API_PREFIX + f"seller/{seller.id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_200_OK

    # Seller update

    response = await async_client.put(
        API_PREFIX + f"seller/{seller.id}",
        json={
            "first_name": NEW_SELLER_1["first_name"],
            "last_name": NEW_SELLER_1["last_name"],
            "email": NEW_SELLER_1["email"],
        },
    )

    assert response.status_code == status.HTTP_200_OK

    # Auth with new email

    new_login_data = {"username": NEW_SELLER_1["email"], "password": ORIGINAL_SELLER_1_PASSWORD}

    response = await async_client.post(API_PREFIX + "token", data=new_login_data)

    assert response.status_code == status.HTTP_200_OK

    access_token = response.json()["access_token"]

    # Seller info

    response = await async_client.get(
        API_PREFIX + f"seller/{seller.id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_200_OK

    # Seller deletion

    response = await async_client.delete(API_PREFIX + f"seller/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
