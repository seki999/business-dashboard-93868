def test_validation_error_does_not_expose_internal_details(client):
    """入力値エラーで DB やスタックトレースが露出しないことを確認します。"""

    response = client.post(
        "/api/deliveries",
        json={
            "delivery_code": "NG",
            "area": "",
            "scheduled_date": "invalid-date",
            "status": "unknown",
            "assignee": "",
        },
    )

    assert response.status_code == 422
    assert "Traceback" not in response.text
