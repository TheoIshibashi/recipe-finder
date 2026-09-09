from fastapi.testclient import TestClient
from app.main import app
from app.mealdb_client import MealDBError

client = TestClient(app)

def test_recipe_by_id(monkeypatch):
    mock_recipe_data = {
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
    }

    async def mock_get_recipe_by_id(recipe_id: str):
        assert recipe_id == "123"
        return mock_recipe_data

    monkeypatch.setattr("app.routes.lookup_by_id", mock_get_recipe_by_id)

    response = client.get("/recipes/123")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == "123"
    assert data["name"] == "Chicken Test"
    assert data["category"] == "Chicken"
    assert data["ingredients"][0]["name"] == "Chicken"

def test_recipe_by_id_not_found(monkeypatch):
    async def mock_get_recipe_by_id(recipe_id: str):
        assert recipe_id == "999"
        return None

    monkeypatch.setattr("app.routes.lookup_by_id", mock_get_recipe_by_id)

    response = client.get("/recipes/999")
    assert response.json() == {"detail": "Receita não encontrada."}
    assert response.status_code == 404

def test_recipe_by_id_mealdb_error(monkeypatch):
    async def mock_get_recipe_by_id(recipe_id: str):
        raise MealDBError("Erro de teste")

    monkeypatch.setattr("app.routes.lookup_by_id", mock_get_recipe_by_id)
    response = client.get("/recipes/123")
    assert response.status_code == 500
    assert response.json() == {"detail": "Erro de teste"}

