from tests.api_client import PetStoreClient
from tests.conftest import random_user_data
import pytest
import allure

api = PetStoreClient()
pytestmark = [
    allure.epic("Swagger Petstore API"),
    allure.feature("(User)")
]

def test_create_user(random_user_data):
    response = api.create_user(payload=random_user_data)
    assert response.status_code == 200



@allure.story("Get user by name")
@allure.title("Successfully get user by name")
def test_get_user_by_name(random_user_data):
    api.create_user(payload=random_user_data)
    response_get_user = api.get_user_by_name(random_user_data["username"])
    user_data_from_server = response_get_user.json()
    with allure.step("Check status-code and user's info"):
        assert response_get_user.status_code == 200
        assert user_data_from_server["email"] == random_user_data["email"]
        assert user_data_from_server["phone"] == random_user_data["phone"]

@allure.story("Update user")
@allure.title("Successfully update user")
def test_update_user(random_user_data):
    response_create_user = api.create_user(payload=random_user_data)
    random_user_data["firstName"] = "Platina"
    username_target = random_user_data["username"]
    response_update = api.update_user(
        username=username_target, payload=random_user_data
    )
    assert response_update.status_code == 200
    response_get = api.get_user_by_name(username_target)
    assert response_get.status_code == 200
    updated_user_from_server = response_get.json()
    assert updated_user_from_server["firstName"] == "Platina"

@allure.story("Delete user")
@allure.title("Successfully delete user")
def test_delete_user(random_user_data):
    response = api.create_user(payload=random_user_data)
    username_target = random_user_data["username"]
    response_delete = api.delete_user(username=username_target)
    assert response_delete.status_code == 200
    response_get = api.get_user_by_name(username_target)
    assert response_get.status_code == 404

@allure.story("Get non-existent user")
@allure.title("Successfully get non-existent user")
@pytest.mark.negative
def test_get_non_existent_user():
    user_name = "fsdfnhnz21451s4"
    response_get_user_by_name = api.get_user_by_name(user_name)
    assert response_get_user_by_name.status_code == 404
    data = response_get_user_by_name.json()
    assert data["message"] == "User not found"

@allure.story("Creating user with invalid data")
@allure.title("Successfully creating user with invalid data")
@pytest.mark.parametrize(
    "broken_field, invalid_value",
    [("password", ""), ("email", "just_mail_no_dog.com"), ("username", "a" * 1000)],
)
@pytest.mark.xfail(reason="Just not validate boundary values and empty values")
def test_create_invalid_user(broken_field, invalid_value, random_user_data):
    random_user_data[broken_field] = invalid_value
    response = api.create_user(payload=random_user_data)
    assert response.status_code == 400
