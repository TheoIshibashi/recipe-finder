from app.schemas import _parse_ingredients, parse_recipe, parse_recipe_summary

def test_parse_ingredients():
    raw = {
        "strIngredient1": " Chicken ",
        "strMeasure1": " 200g ",
    }
    ingredients = _parse_ingredients(raw)
    assert len(ingredients) == 1
    assert ingredients[0].name == "Chicken"
    assert ingredients[0].measure == "200g"

def test_parse_ingredients_empty():
    raw = {
        "strIngredient1": "Chicken",
        "strMeasure1": "200g",
        "strIngredient2": "",
        "strMeasure2": "1 cup"
    }
    ingredients = _parse_ingredients(raw)
    assert len(ingredients) == 1
    assert ingredients[0].name == "Chicken"
    assert ingredients[0].measure == "200g"

def test_parse_ingredients_empty_measure():
    raw = {
        "strIngredient1": "Chicken",
        "strMeasure1": ""
    }

    ingredients = _parse_ingredients(raw)
    assert len(ingredients) == 1
    assert ingredients[0].name == "Chicken"
    assert ingredients[0].measure is None

def test_parse_ingredients_none():
    raw = {
        "strIngredient1": None,
        "strMeasure1": "200g",
    }

    ingredients = _parse_ingredients(raw)
    assert len(ingredients) == 0

def test_parse_ingredients_multiple():
     raw = {
            "strIngredient1": "Chicken",
            "strMeasure1": "200g",
            "strIngredient2": "Rice",
            "strMeasure2": "1 cup",
            "strIngredient3": None,
            "strMeasure3": None,
        }

     ingredients = _parse_ingredients(raw)
     assert len(ingredients) == 2
     assert ingredients[0].name == "Chicken"
     assert ingredients[0].measure == "200g"
     assert ingredients[1].name == "Rice"
     assert ingredients[1].measure == "1 cup"

def test_parse_recipe():
    raw = {
        "idMeal": "123",
        "strMeal": "Chicken Test",
        "strCategory": "Chicken",
        "strArea": "Test",
        "strInstructions": "Cook it.",
        "strMealThumb": None,
        "strYoutube": None,
        "strTags": "Chicken, Dinner, Easy",
        "strIngredient1": "Chicken",
        "strMeasure1": "200g",
        "strIngredient2": "Rice",
        "strMeasure2": "1 cup"
    }

    recipe = parse_recipe(raw)
    assert recipe.id == "123"
    assert recipe.name == "Chicken Test"
    assert recipe.category == "Chicken"
    assert recipe.tags == ["Chicken", "Dinner", "Easy"]
    assert len(recipe.ingredients) == 2
    assert recipe.ingredients[0].name == "Chicken"
    assert recipe.ingredients[0].measure == "200g"
    assert recipe.ingredients[1].name == "Rice"
    assert recipe.ingredients[1].measure == "1 cup"

def test_parse_recipe_summary():
    raw = {
        "idMeal": "123",
        "strMeal": "Chicken Test",
        "strMealThumb": "https://example.com/chicken.jpg",
    }

    recipe = parse_recipe_summary(raw)
    assert recipe.id == "123"
    assert recipe.name == "Chicken Test"
    assert recipe.thumbnail == "https://example.com/chicken.jpg"