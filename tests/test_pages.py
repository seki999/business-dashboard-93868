def test_html_pages_render(client):
    """README スクリーンショット対象の画面が HTML として表示できることを確認します。"""

    for path in ["/", "/deliveries", "/feedbacks", "/batch", "/logs"]:
        response = client.get(path)

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
