import pytest
import requests
import json


baseUrl = "http://localhost:8000"
auth_body = {"username": "test", "password": "1234"}
json_body = {"data": [{"key": "key1", "val": "val1", "valType": "str"}]}
myToken = '{ "access_token":"ververylongstringwithnumbersandstuff"}'
head = {'Content-Type': 'application/json','Authorization': 'Bearer {}'.format(myToken)}
auth_head = {'Content-Type': 'application/json'}
path = "/api/poly"
auth = "/api/auth"
errMsg = "Not Found"


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class TestData:
    id: int = 0
    token: int = 0


@pytest.fixture
def test_data() -> TestData:
    return TestData()


class TestApi:
    def test_auth(self, test_data: TestData):
        auth_resp = requests.post(url=f"{baseUrl}{auth}", headers=auth_head,  data=json.dumps(auth_body))
        assert auth_resp.status_code == 200
        auth_resp_data = json.loads(auth_resp.text)
        test_data.token = auth_resp_data["access_token"]

    def test_create_user(self, test_data: TestData):
        header = self.get_header(test_data.token)
        response = requests.post(url=f"{baseUrl}{path}", headers=header, data=json.dumps(json_body))
        response_json = json.loads(response.text)
        assert response.status_code == 200
        assert response_json["values"][0]["key"] == json_body["data"][0]["key"]
        assert response_json["values"][0]["val"] == json_body["data"][0]["val"]
        assert response_json["values"][0]["valType"] == json_body["data"][0]["valType"]
        test_data.id = response_json["id"]

    def test_fetch_user(self, test_data: TestData):
        header = self.get_header(test_data.token)
        response = requests.get(url=f"{baseUrl}{path}/{test_data.id}", headers=header)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        assert response_json["data"][0]["key"] == json_body["data"][0]["key"]
        assert response_json["data"][0]["val"] == json_body["data"][0]["val"]
        assert response_json["data"][0]["valType"] == json_body["data"][0]["valType"]
        print(1)

    def test_delete_user(self, test_data: TestData):
            header = self.get_header(test_data.token)
            response = requests.delete(url=f"{baseUrl}{path}/{test_data.id}", headers=header)
            assert response.status_code == 200
            response = requests.get(url=f"{baseUrl}{path}/{test_data.id}", headers=header)
            response_json = json.loads(response.text)
            assert response.status_code == 404
            assert response_json["error"] == errMsg

    def get_header(self, token):
        return {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
