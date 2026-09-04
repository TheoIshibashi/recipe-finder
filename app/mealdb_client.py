import httpx
from app.config import settings


class MealDBError(Exception):
    """Erro de comunicação com a TheMealDB (timeout, API fora do ar, etc)."""


BASE_URL = f"https://www.themealdb.com/api/json/v1/{settings.MEALDB_API_KEY}"


async def _get(endpoint: str, params: dict) -> dict:
    url = f"{BASE_URL}/{endpoint}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # lança exceção se status >= 400
            return response.json()
    except httpx.TimeoutException as exc:
        raise MealDBError("A TheMealDB demorou demais para responder.") from exc
    except httpx.HTTPStatusError as exc:
        raise MealDBError(
            f"TheMealDB retornou erro {exc.response.status_code}."
        ) from exc
    except httpx.RequestError as exc:
        raise MealDBError("Não foi possível conectar à TheMealDB.") from exc


async def search_by_name(name: str) -> list[dict]:
    data = await _get("search.php", {"s": name})
    return data.get("meals") or []


async def lookup_by_id(meal_id: str) -> dict | None:
    data = await _get("lookup.php", {"i": meal_id})
    meals = data.get("meals") or []
    return meals[0] if meals else None


async def random_meal() -> dict | None:
    """Retorna uma receita aleatória completa."""
    data = await _get("random.php", {})
    meals = data.get("meals") or []
    return meals[0] if meals else None


async def filter_by_ingredient(ingredient: str) -> list[dict]:
    """
    Filtra receitas que usam `ingredient`. ATENÇÃO: essa resposta vem
    incompleta (só id, nome e thumbnail) — a API grátis não devolve
    ingredientes/instruções nesse endpoint. Pra ter os detalhes completos,
    quem chamar essa função precisa depois usar `lookup_by_id` no id
    de cada resultado que interessar.
    """
    data = await _get("filter.php", {"i": ingredient})
    return data.get("meals") or []


async def list_categories() -> list[dict]:
    """Lista todas as categorias disponíveis (ex: Vegetarian, Seafood)."""
    data = await _get("categories.php", {})
    return data.get("categories") or []