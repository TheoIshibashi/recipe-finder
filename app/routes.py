from fastapi import APIRouter, HTTPException
from app.mealdb_client import random_meal, MealDBError
from app.schemas import Recipe, parse_recipe

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

