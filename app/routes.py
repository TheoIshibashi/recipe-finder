from fastapi import APIRouter, HTTPException
from app.mealdb_client import random_meal, MealDBError, lookup_by_id, search_by_name, RecipeSummary, filter_by_ingredient
from app.schemas import Recipe, parse_recipe, parse_recipe_summary

router = APIRouter()

@router.get("/recipes/random", response_model=Recipe)
async def get_random_meal() -> Recipe:
    try:
        meal_data = await random_meal()
        if meal_data is None:
            raise HTTPException(status_code=404, detail="Nenhuma receita aleatória encontrada.")
        return parse_recipe(meal_data)
    except MealDBError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recipes/search", response_model=list[Recipe])
async def search_recipes(name: str) -> list[Recipe]:
    try:
        meal_data_list = await search_by_name(name)
        return [parse_recipe(meal_data) for meal_data in meal_data_list]
    except MealDBError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recipes/by_ingredient", response_model=list[RecipeSummary])
async def get_recipes_by_ingredient(ingredient: str) -> list[RecipeSummary]:
    try:
        meal_data_list = await filter_by_ingredient(ingredient)
        return [parse_recipe_summary(meal_data) for meal_data in meal_data_list]
    except MealDBError as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe_by_id(recipe_id: str) -> Recipe:
    try:
        meal_data = await lookup_by_id(recipe_id)
        if meal_data is None:
            raise HTTPException(status_code=404, detail="Receita não encontrada.")
        return parse_recipe(meal_data)
    except MealDBError as e:
        raise HTTPException(status_code=500, detail=str(e))



        