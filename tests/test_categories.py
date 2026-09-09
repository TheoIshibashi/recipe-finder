from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_categories(monkeypatch):
    mock_categories = [
        {"idCategory": "1", "strCategory": "Beef"},
        {"idCategory": "2", "strCategory": "Chicken"},
    ]

    async def mock_list_categories():
        return mock_categories
    
    monkeypatch.setattr("app.routes.list_categories", mock_list_categories)

    response = client.get("/categories")
    assert response.status_code == 200
    assert response.json() == mock_categories