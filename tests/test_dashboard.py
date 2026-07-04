def test_dashboard_api(client):
    """ダッシュボード API が主要 KPI を返すことを確認します。"""

    response = client.get("/api/dashboard")
    payload = response.json()

    assert response.status_code == 200
    assert "today_orders" in payload
    assert "recent_logs" in payload
