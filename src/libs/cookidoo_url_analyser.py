from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from rich.console import Console
from unicodedata import numeric
from libs.recipe_class import Recipe, Ingredient
import re

console = Console()

ingredient_pattern = re.compile(r"((?P<name>[\w\ \-,\.]+){1}\n{0,1}(?P<description>[\w\ \-,(\.]+[\d]*[\w)]+\n){0,1}((?P<quantity>[\d\u00BC-\u00BE\u2150-\u215E]+){1}\s*(?P<unit>\w+){0,1}){0,1}\s*)", re.M)

def analyse_cookidoo_url(url: str) -> dict | None:
    recipe = Recipe()
    console.print(f"Analyzing Cookidoo URL: {url}", style="bold blue")

    driver = webdriver.WebDriver()  # Initialize the Selenium WebDriver (make sure to have the appropriate driver installed)
    try:
        driver.get(url)  # Open the URL in the browser
    except Exception as e:
        console.print(f"Error accessing the URL: {e}", style="bold red")
        driver.quit()
        return None
    
    console.print("Loaded the recipe page successfully.", style="bold green")
    console.print("Fetching recipe title and ingredients...", style="bold yellow")

    try:
        recipe.name = driver.find_element("class name", "recipe-card__name").text
        console.print(f"Recipe content: {recipe.__str__()}", style="bold green")
    except Exception as e:
        console.print(f"Error fetching recipe name: {e}", style="bold red")
        driver.quit()
        return None
    
    try:
        ingredients = driver.find_elements(By.TAG_NAME, "recipe-ingredient")
        for ingredient in ingredients:
            console.print(f"Processing ingredient: {ingredient.text.strip()}", style="bold cyan")
            result = re.search(ingredient_pattern, ingredient.text.strip())

            if not result:
                console.print(f"Failed to parse ingredient: {ingredient.text.strip()}", style="bold red")
                continue

            ingredient_name = result.group("name").strip()
            #console.print(f"Found ingredient: {ingredient_name}", style="bold cyan")
            quantity = result.group("quantity").strip() if result.group("quantity") else None
            #console.print(f"Quantity: {quantity}", style="bold cyan")
            unit = result.group("unit").strip() if result.group("unit") else "Stück"
            #console.print(f"Unit: {unit}", style="bold cyan")
            description = result.group("description").strip() if result.group("description") else None

            if not quantity:
                quantity = 1
            elif quantity.isdigit():
                quantity = int(quantity)
            else:
                try:
                    quantity = numeric(quantity)
                except ValueError:
                    console.print(f"Invalid quantity format for ingredient: {ingredient_name}. Defaulting to 1.", style="bold red")
                    quantity = 1

            recipe.add_ingredient(Ingredient(name=ingredient_name, quantity=float(quantity), unit=unit, description=description))
            console.print(f"Added ingredient: {ingredient_name} - {quantity} {unit}", style="bold green")
    except Exception as e:
        print(f"Error fetching ingredients: {e}")
        driver.quit()
        exit(1)
    
    
    return recipe.model_dump()