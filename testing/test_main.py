from fastapi.testclient import TestClient
from app.main import app
from time import sleep

client = TestClient(app)
# pastikan table item kosong dan belum pernah insert data sebelumnya
# atau truncate table terlebih dahulu
data = {"id": 1, "name": "Foo Bar", "stock": 2000}
data2 = {"id": 2, "name": "Foo Bar", "stock": 2000}

# testing api untuk membuat data item baru


def test_create_item():
    response = client.post(
        "api/v1/items/",
        json=data,
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Item Created", "data": data}

# testing race condition menggunakan API update dengan Transaction
def test_race_condition(start_race):
    def actual_test():  # function untuk simulasi race condition
        client.patch(
            "api/v1/items/update_stock/1",
            json={
                "stock": 200
            },
        )
    # thread_num adalah jumlah thread yang mengakses API secara bersamaan
    start_race(threads_num=10, target=actual_test)

    # cek hasil update data apakah terpengaruh thread lain
    response = client.get(
        "api/v1/items/1"
    )
    assert response.json() == {
        "id": 1,
        "name": "Foo Bar",
        "stock": 1800
    }


def test_create_item2():
    response = client.post(
        "api/v1/items/",
        json=data,
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Item Created", "data": data2}

# testing race condition menggunakan API update tanpa Transaction
def test_race_condition2(start_race):
    def actual_test():
        client.patch(
            "api/v1/items/update_stock_race/2",
            json={
                "stock": 200
            },
        )

    start_race(threads_num=10, target=actual_test)

    # cek hasil update data apakah terpengaruh thread lain
    response = client.get(
        "api/v1/items/2"
    )
    assert response.json() != {
        "id": 2,
        "name": "Foo Bar",
        "stock": 1800
    }



