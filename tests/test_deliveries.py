def test_delivery_create_and_list(client):
    """配送データの登録と一覧取得ができることを確認します。"""

    payload = {
        "delivery_code": "D-TEST-001",
        "area": "Test Area",
        "scheduled_date": "2026-07-04",
        "status": "scheduled",
        "assignee": "Test Team",
        "note": "pytest sample",
    }

    create_response = client.post("/api/deliveries", json=payload)
    list_response = client.get("/api/deliveries")

    assert create_response.status_code == 201
    assert create_response.json()["delivery_code"] == "D-TEST-001"
    assert list_response.status_code == 200
    assert any(item["delivery_code"] == "D-TEST-001" for item in list_response.json())


def test_delivery_duplicate_returns_business_error(client):
    """重複コードが内部エラーではなく業務エラーとして返ることを確認します。"""

    payload = {
        "delivery_code": "D-TEST-DUP",
        "area": "Test Area",
        "scheduled_date": "2026-07-04",
        "status": "scheduled",
        "assignee": "Test Team",
        "note": None,
    }

    assert client.post("/api/deliveries", json=payload).status_code == 201
    duplicate_response = client.post("/api/deliveries", json=payload)

    assert duplicate_response.status_code == 409
    assert duplicate_response.json()["detail"] == "delivery_code already exists"
