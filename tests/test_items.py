def test_create_item(client):
    response = client.post(
        "/api/v1/items",
        json={"id": 1, "name": "Test Item", "description": "This is a test"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Item"


def test_get_items(client):
    response = client.get("/api/v1/items")
    assert response.status_code == 200

    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 1


def test_delete_item(client):
    # create first
    client.post(
        "/api/v1/items",
        json={"id": 2, "name": "Delete Me", "description": "Remove this item"},
    )

    # delete it
    response = client.delete("/api/v1/items/2")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}
