import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def random_pet_data():
    return {
        "id": fake.random_int(min=10000, max=99999),
        "category": {"id": 1, "name": "Dogs"},
        "name": fake.first_name(),
        "photoUrls": ["https://example.com/photo.jpg"],
        "tags": [{"id": 1, "name": "cute"}],
        "status": "available",
    }


@pytest.fixture
def random_order_data():
    return {
        "id": fake.random_int(min=1, max=10),
        "petId": fake.random_int(min=1000, max=99999),
        "quantity": fake.random_int(min=10, max=3000),
        "shipDate": "2026-03-12T07:22:26.871Z",
        "status": "placed",
        "complete": fake.boolean(),
    }


@pytest.fixture
def random_user_data():
    return {
        "id": fake.random_int(min=1000, max=20000),
        "username": fake.user_name(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(),
        "phone": fake.phone_number(),
        "userStatus": 0,
    }
