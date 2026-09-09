from fastapi.testclient import TestClient
from app.main import app
from app.mealdb_client import MealDBError

client = TestClient(app)

def test_random_recipe(monkeypatch):
    mock_random_recipe_data = {
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

    async def mock_random_meal():
        return mock_random_recipe_data

    monkeypatch.setattr("app.routes.random_meal", mock_random_meal)
    response = client.get("/recipes/random")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == "123"
    assert data["name"] == "Chicken Test"
    assert data["category"] == "Chicken"
    assert data["area"] == "Test"
    assert data["instructions"] == "Cook it."
    assert data["ingredients"][0]["name"] == "Chicken"

def test_random_meal_is_not_found(monkeypatch):
    async def mock_random_meal_is_not_found():
        return None

    monkeypatch.setattr("app.routes.random_meal", mock_random_meal_is_not_found)
    response = client.get("/recipes/random")
    assert response.json() == {"detail": "Nenhuma receita aleatória encontrada."}
    assert response.status_code == 404

def test_random_meal_mealdb_error(monkeypatch):
    async def mock_random_meal_mealdb_error():
        raise MealDBError("Erro de teste")

    monkeypatch.setattr("app.routes.random_meal", mock_random_meal_mealdb_error)
    response = client.get("/recipes/random")
    assert response.status_code == 500
    assert response.json() == {"detail": "Erro de teste"}

