from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_by_ingredient(monkeypatch):
    mock_ingredients = [
        {"idMeal": "123", 
         "strMeal": "Chicken Test",
         "strMealThumb": None},
    ]

    async def mock_filter_by_ingredient(ingredient: str):
        assert ingredient == "chicken"
        return mock_ingredients

    monkeypatch.setattr("app.routes.filter_by_ingredient", mock_filter_by_ingredient)

    response = client.get("/recipes/by-ingredient?ingredient=chicken")
    data = response.json()
    assert response.status_code == 200
    assert data[0]["id"] == "123"
    assert data[0]["name"] == "Chicken Test"
    assert data[0]["thumbnail"] is None

def test_search_route():
    response = client.get("/recipes/search?ingredients=")
    assert response.status_code == 422

def test_search_route_only_spaces():
    response = client.get("/recipes/search?ingredients=%20%20%20")
    assert response.status_code == 422