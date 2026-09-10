from app.mealdb_client import MealDBError

def test_categories(client,monkeypatch):
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

def test_categories_mealdb_error(client, monkeypatch):
    async def mock_list_categories():
        raise MealDBError("Erro de teste")

    monkeypatch.setattr("app.routes.list_categories", mock_list_categories)
    response = client.get("/categories")
    assert response.status_code == 500
    assert response.json() == {"detail": "Erro de teste"}
