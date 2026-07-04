def test_batch_run(client):
    """手動バッチ実行 API が結果サマリを返すことを確認します。"""

    response = client.post("/api/batch/run")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "completed"
    assert "low_stock_products" in payload
