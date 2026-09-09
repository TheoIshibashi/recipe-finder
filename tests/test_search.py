from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_recipes(monkeypatch):
    mock_meal_data_list = [{
    "idMeal": "123",
    "strMeal": "Chicken Test",
    "strCategory": "Chicken",
    "strArea": "Test",
    "strInstructions": "Cook it.",
    "strMealThumb": None,
    "strYoutube": None,
    "strTags": None,
    "strIngredient1": "Chicken",
    "strMeasure1": "200g",
    }]

    async def mock_search_by_name(name: str):
        assert name == "chicken"
        return mock_meal_data_list

    monkeypatch.setattr("app.routes.search_by_name", mock_search_by_name)

    response = client.get("/recipes/search?name=chicken")
    data = response.json()
    assert response.status_code == 200
    assert data[0]["id"] == "123"
    assert data[0]["name"] == "Chicken Test"
    assert data[0]["category"] == "Chicken"
    assert data[0]["ingredients"][0]["name"] == "Chicken"
    assert data[0]["ingredients"][0]["measure"] == "200g"