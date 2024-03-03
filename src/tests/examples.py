from src.auth.security import get_password_hash

# Original seller data
ORIGINAL_SELLER_1_PASSWORD = "password_1"
ORIGINAL_SELLER_1_HASHED = {
    "first_name": "Original_Seller_1",
    "last_name": "Original_Seller_1",
    "email": "original_seller_1@seller.seller",
    "hashed_password": get_password_hash(ORIGINAL_SELLER_1_PASSWORD),
}
ORIGINAL_SELLER_1 = {
    "first_name": "Original_Seller_1",
    "last_name": "Original_Seller_1",
    "email": "original_seller_1@seller.seller",
    "hashed_password": ORIGINAL_SELLER_1_PASSWORD,
}

ORIGINAL_SELLER_2_PASSWORD = "password_2"
ORIGINAL_SELLER_2_HASHED = {
    "first_name": "Original_Seller_2",
    "last_name": "Original_Seller_2",
    "email": "original_seller_2@seller.seller",
    "hashed_password": get_password_hash(ORIGINAL_SELLER_2_PASSWORD),
}
ORIGINAL_SELLER_2 = {
    "first_name": "Original_Seller_2",
    "last_name": "Original_Seller_2",
    "email": "original_seller_2@seller.seller",
    "hashed_password": ORIGINAL_SELLER_2_PASSWORD,
}

# API prefix
API_PREFIX = "/api/v1/"

# New seller data
NEW_SELLER_1 = {
    "first_name": "New_Seller_1",
    "last_name": "New_Seller_1",
    "email": "new_seller_1@seller.seller",
}