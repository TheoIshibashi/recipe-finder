from pydantic import BaseModel

class RecipeIngredient(BaseModel):
    name: str
    measure: str | None = None

class Recipe(BaseModel):
    id: str
    name: str
    category: str | None = None
    area: str | None = None
    instructions: str
    thumbnail: str | None = None
    youtube: str | None = None
    tags: list[str] = []
    ingredients: list[RecipeIngredient] = []

class RecipeSummary(BaseModel):
    id: str
    name: str
    thumbnail: str | None = None

def _parse_ingredients(raw: dict) -> list[RecipeIngredient]:
    """
    A TheMealDB manda os ingredientes em 20 pares de campos fixos:
    strIngredient1/strMeasure1, strIngredient2/strMeasure2, ... até 20.
    A maioria vem vazia ("") ou null, porque a maior parte das receitas
    usa bem menos que 20 ingredientes. Aqui a gente varre os 20 e só
    guarda os que têm nome de verdade.
    """
    ingredients = []
    for i in range(1, 21):
        name = raw.get(f"strIngredient{i}")
        measure = raw.get(f"strMeasure{i}")
 
        # Precisa checar as DUAS coisas: se é None (campo não veio) E se,
        # depois de tirar espaços, não sobrou string vazia. A API mistura
        # os dois casos (às vezes manda "", às vezes manda null) então só
        # checar "if name" já cobriria ambos, mas deixo explícito por clareza.
        if name is None or not name.strip():
            continue
 
        ingredients.append(
            RecipeIngredient(
                name=name.strip(),
                # measure pode ser "" (string vazia) — nesse caso queremos
                # None no nosso modelo, não uma string vazia sem sentido.
                measure=measure.strip() if measure and measure.strip() else None,
            )
        )
    return ingredients
 
 
def parse_recipe(raw: dict) -> Recipe:
    """Transforma o JSON cru de UMA receita (de lookup.php, search.php ou
    random.php) no nosso modelo Recipe, já limpo."""
    tags_raw = raw.get("strTags")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
 
    return Recipe(
        id=raw["idMeal"],
        name=raw["strMeal"],
        category=raw.get("strCategory"),
        area=raw.get("strArea"),
        instructions=raw.get("strInstructions") or "",
        thumbnail=raw.get("strMealThumb"),
        youtube=raw.get("strYoutube") or None,
        tags=tags,
        ingredients=_parse_ingredients(raw),
    )
 
 
def parse_recipe_summary(raw: dict) -> RecipeSummary:
    """Transforma o JSON cru e INCOMPLETO que vem de filter.php (só tem
    id, nome e thumbnail) no nosso modelo RecipeSummary."""
    return RecipeSummary(
        id=raw["idMeal"],
        name=raw["strMeal"],
        thumbnail=raw.get("strMealThumb"),
    )
