import pydantic

class Ingredient(pydantic.BaseModel):
    """
    A class representing an ingredient with its name and quantity.
    """
    name: str
    quantity: int | float  # Quantity can be a string to accommodate various formats (e.g., "2 cups", "1 tbsp")
    unit: str = {"EL", "TL", "g", "kg", "L", "ml"}  # Unit of measurement (e.g., "cups", "tbsp")
    description: str | None = None  # Optional description of the ingredient

    def __str__(self):
        return f"Ingredient(name={self.name}, quantity={self.quantity} {self.unit})"

class Recipe(pydantic.BaseModel):
    """
    A class representing a recipe with its ingredients and their quantities.
    """
    name: str | None = None 
    ingredients: list[Ingredient] = []  # List of Ingredient objects

    def add_ingredient(self, ingredient: Ingredient):
        """
        Add an ingredient to the recipe.
        :param ingredient: An instance of Ingredient to be added.
        """
        if not isinstance(ingredient, Ingredient):
            raise TypeError("ingredient must be an instance of Ingredient")
        self.ingredients.append(ingredient)

    def __str__(self):
        return f"Recipe(name={self.name}, ingredients={self.ingredients})"