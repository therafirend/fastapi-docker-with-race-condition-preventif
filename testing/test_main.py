from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

data = {"id": 1, "name": "Foo Bar", "stock": 2000}


# def test_create_item():
#     response = client.post(
#         "api/v1/items/",
#         json=data,
#     )
#     assert response.status_code == 201
#     assert response.json() == {"message": "Item Created", "data": data}
#

def test_race_condition(start_race):
    def actual_test():
        client.patch(
            "api/v1/items/1/checkout",
            json={
                "stock": 20
            },
        )

    start_race(threads_num=5, target=actual_test)
    response = client.get(
        "api/v1/items/1"
    )
    assert response.json() == {
        "id": 1,
        "name": "Foo Bar",
        "stock": 1980
    }
