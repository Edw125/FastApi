from fastapi.testclient import TestClient

from server import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.request.method == 'GET'
    with open('templates/home.html', 'r') as html:
        assert response.text == html.read().strip()
