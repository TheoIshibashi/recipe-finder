from fastapi.testclient import TestClient
from app.main import app
from app.mealdb_client import MealDBError

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

def test_categories_mealdb_error(monkeypatch):
    async def mock_list_categories():
        raise MealDBError("Erro de teste")

    monkeypatch.setattr("app.routes.list_categories", mock_list_categories)
    response = client.get("/categories")
    assert response.status_code == 500
    assert response.json() == {"detail": "Erro de teste"}
