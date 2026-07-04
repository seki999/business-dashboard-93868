def test_health_check(client):
    """ヘルスチェック API が監視で利用できる形式を返すことを確認します。"""

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
