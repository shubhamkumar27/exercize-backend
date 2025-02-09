import time

def test_create_order_success(client):
    order_data = {
        "type": "limit",
        "side": "buy",
        "instrument": "AAPL12345678",
        "limit_price": 150.50,
        "quantity": 10
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 201
    assert response.json()["status"] == "pending"

def test_create_order_failed_validation_quantity(client):
    order_data = {
        "type": "market",
        "side": "buy",
        "instrument": "AAPL12345678",
        "limit_price": 150.50,
        "quantity": 0
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 422

def test_create_order_failed_validation_type_market(client):
    order_data = {
        "type": "market",
        "side": "buy",
        "instrument": "AAPL12345678",
        "limit_price": 150.50,
        "quantity": 10
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Providing a `limit_price` is prohibited for type `market`"

def test_create_order_failed_validation_type_limit(client):
    order_data = {
        "type": "limit",
        "side": "buy",
        "instrument": "AAPL12345678",
        "limit_price": 0,
        "quantity": 10
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Attribute `limit_price` is required for type `limit`"

def test_get_order_success(client):
    order_data = {
        "type": "limit",
        "side": "buy",
        "instrument": "AAPL12345678",
        "limit_price": 150.50,
        "quantity": 10
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 201
    assert response.json()["status"] == "pending"

    time.sleep(1)
    order_id = response.json()["id"]
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id
    assert response.json()["status"] == "placed"

def test_get_order_not_found(client):
    response = client.get(f"/orders/unknown")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"