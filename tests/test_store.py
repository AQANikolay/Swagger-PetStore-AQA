from tests.api_client import PetStoreClient
from tests.conftest import random_order_data
import pytest
import allure

api = PetStoreClient()

pytestmark = [
    allure.epic("Swagger Petstore API"),
    allure.feature("(Store)")
]
@allure.story("Get store inventory")
@allure.title("Successfully get story inventory")
@pytest.mark.positive
def test_store_inventory():
    response = api.get_pet_inventory()
    assert response.status_code == 200
    assert len(response.json()) > 0

@allure.story("Create order")
@allure.title("Successfully create order")
@pytest.mark.positive
def test_create_order(random_order_data):
    response = api.create_order(payload=random_order_data)
    with allure.step("Check status-code and order info"):
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == random_order_data["id"]
        assert data["petId"] == random_order_data["petId"]
        assert data["complete"] == random_order_data["complete"]

@allure.story("Get order by id")
@allure.title("Successfully get order by id")
@pytest.mark.positive
def test_get_order_by_id(random_order_data):
    response_create = api.create_order(payload=random_order_data)
    data_create = response_create.json()
    response_get_by_id = api.get_order_by_id(data_create["id"])
    data_by_id = response_get_by_id.json()
    with allure.step("Check equals id"):
        assert data_create["id"] == data_by_id["id"]

@allure.story("Delete order")
@allure.title("Successfully delete order")
@pytest.mark.positive
def test_delete_order(random_order_data):
    response_create = api.create_order(payload=random_order_data)
    data_create = response_create.json()
    response_delete = api.delete_order(data_create["id"])
    response_check = api.get_order_by_id(data_create["id"])
    with allure.step("Check status-code"):
        assert response_delete.status_code == 200
        assert response_check.status_code == 404

@allure.story("Create empty order")
@allure.title("Creating empty order")
@pytest.mark.xfail(reason="BackEnd bug doesn't validate empty values")
def test_create_order_empty_payload():
    response = api.create_order(payload={})
    with allure.step("Check status-code"):
        assert response.status_code == 400

@allure.story("Creating order with invalid quantity")
@allure.title("Successfully creating order with invalid quantity")
@pytest.mark.parametrize(
    "quantity, invalid_value",
    [
        ("quantity", -1),
        ("quantity", 0),
        ("quantity", 99999999999999999999999999),
    ],
)
@pytest.mark.xfail(reason="Smth with database")
def test_create_order_with_invalid_quantity(quantity, invalid_value, random_order_data):
    random_order_data["quantity"] = invalid_value
    response = api.create_order(payload=random_order_data)
    with allure.step("Check status-code"):
        assert response.status_code == 400
