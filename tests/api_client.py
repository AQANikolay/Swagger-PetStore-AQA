import allure
import json
import requests


class PetStoreClient:
    def __init__(self):
        self.base_url = "https://petstore.swagger.io/v2/"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _make_request(self, method, url, **kwargs):
        with allure.step(f"Request: {method} {url}"):
            if "json" in kwargs:
                payload_str = json.dumps(kwargs["json"], indent=4)
                allure.attach(
                    payload_str,
                    name="Request JSON",
                    attachment_type=allure.attachment_type.JSON,
                )
            response = requests.request(method, url, **kwargs)
            allure.attach(
                response.text,
                name="Response BODY",
                attachment_type=allure.attachment_type.JSON,
            )
            return response

    def get_pet_by_status(self, params):
        url = f"{self.base_url}pet/findByStatus?status={params}"
        return self._make_request("GET", url, params=params, headers=self.headers)

    def create_new_pet(self, payload):
        url = f"{self.base_url}pet"
        return self._make_request("POST", url, json=payload, headers=self.headers)

    def get_pet_by_id(self, pet_id):
        url = f"{self.base_url}pet/{pet_id}"
        return self._make_request("GET", url, headers=self.headers)

    def delete_pet(self, pet_id, api_key="special-key"):
        url = f"{self.base_url}pet/{pet_id}"
        custom_headers = self.headers.copy()
        custom_headers["api_key"] = api_key
        return self._make_request("DELETE", url,  headers=custom_headers)

    def get_pet_inventory(self):
        url = f"{self.base_url}store/inventory"
        return self._make_request("GET", url, headers=self.headers)

    def create_order(self, payload):
        url = f"{self.base_url}store/order"
        return self._make_request("POST", url, json=payload, headers=self.headers)

    def get_order_by_id(self, order_id):
        url = f"{self.base_url}store/order/{order_id}"
        return self._make_request("GET", url, headers=self.headers)

    def delete_order(self, order_id):
        url = f"{self.base_url}store/order/{order_id}"
        return self._make_request("DELETE", url, headers=self.headers)

    def create_user(self, payload):
        url = f"{self.base_url}user"
        return self._make_request("POST", url, json=payload, headers=self.headers)

    def get_user_by_name(self, username):
        url = f"{self.base_url}user/{username}"
        return self._make_request("GET", url, headers=self.headers)

    def update_user(self, payload, username):
        url = f"{self.base_url}user/{username}"
        return self._make_request("PUT", url, json=payload, headers=self.headers)

    def delete_user(self, username):
        url = f"{self.base_url}user/{username}"
        return self._make_request("DELETE", url, headers=self.headers)

    def upload_pet_image(self, pet_id, file_path):
        with open(file_path, "rb") as image_file:
            return requests.post(
                f"{self.base_url}pet/{pet_id}/uploadImage", files={"file": image_file}
            )
