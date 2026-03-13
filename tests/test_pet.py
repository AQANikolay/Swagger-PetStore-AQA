import pytest
from faker import Faker
from tests.api_client import PetStoreClient
import allure
import json

api_client = PetStoreClient()
fake = Faker()
pytestmark = [
    allure.epic("Swagger Petstore API"),
    allure.feature("(Pet)")
]
@allure.story("Get Pet")
@allure.title("Successfully get pet by id")
@pytest.mark.positive
def test_get_pet_by_status():
    response = api_client.get_pet_by_status("pending")
    with allure.step("Check status-code, check if length of our response isn't 0"):
        assert response.status_code == 200
        assert type(response.json()) == list
        assert len(response.json()) > 0
        assert response.json()[0]["status"] == "pending"



@allure.story("Creating Pet")
@allure.title("Successfully created Pet")
@pytest.mark.positive
def test_create_new_pet(random_pet_data):
    with allure.step("Step 1: Sending a request to create new pet"):
        data_to_send = random_pet_data
        body_to_attach = json.dumps(data_to_send, indent=4)
        allure.attach(body_to_attach, name="Just've sent (Request)"),
        attachment_type = allure.attachment_type.JSON
        response = api_client.create_new_pet(payload=data_to_send)
    with allure.step("Step 2: Check if status-code equals 200"):
        allure.attach(
            body=response.text,
            name="Response JSON",
            attachment_type=allure.attachment_type.JSON,
        )
        assert response.status_code == 200
    with allure.step(
        "Step 3: Check if pet id equals random pet id and pet name equals random pet name"
    ):
        data = response.json()
        assert data["id"] == random_pet_data["id"]
        assert data["name"] == random_pet_data["name"]

@allure.story("E2E cycle: creating new pet, check if it was created then delete")
@allure.title("E2E cycle")
@pytest.mark.e2e
def test_e2e_pet_cycle():
    random_id = fake.random_int(min=1000, max=9500000)
    random_name = fake.name()
    payload = {
        "id": random_id,
        "category": {"id": 0, "name": "string"},
        "name": random_name,
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "string"}],
        "status": "available",
    }
    response_create = api_client.create_new_pet(payload)
    response_create_data = response_create.json()
    response_get_by_id = api_client.get_pet_by_id(response_create_data["id"])
    response_delete = api_client.delete_pet(response_create_data["id"])
    response_get_by_id_final = api_client.get_pet_by_id(response_create_data["id"])
    with allure.step("Check status-code"):
        assert response_get_by_id_final.status_code == 404

@allure.story("Get Pet by id")
@allure.title("Invalid get pet by id")
@pytest.mark.negative
def test_get_pet_invalid_id():
    pet_id = "@!#$tf"
    api_client.get_pet_by_id(pet_id)
    response_get_pet_by_id = api_client.get_pet_by_id(pet_id)
    with allure.step("Check status-code and if we have message in our response"):
        assert response_get_pet_by_id.status_code == 404
        data = response_get_pet_by_id.json()
        assert "message" in data

@allure.story("Get Pet by status")
@allure.title("Successfully get pet by status")
@pytest.mark.parametrize(
    "target_status",
    [
        "sold",
        "pending",
        "available",
    ],
)
def test_get_pet_by_status_with_loop(target_status):
    response = api_client.get_pet_by_status(target_status)
    with allure.step("Check status-code and response time"):
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert response.elapsed.total_seconds() < 2.0, "Too slow"
        for i in data:
            assert i["status"] == target_status


def test_upload_pet_image(random_pet_data):
    response_create = api_client.create_new_pet(payload=random_pet_data)
    response_photo = api_client.upload_pet_image(
        pet_id=random_pet_data["id"], file_path="test_data/dog.jpeg"
    )
    assert response_photo.status_code == 200
    response_photo_data = response_photo.json()
    assert "additionalMetadata" in response_photo_data["message"]
