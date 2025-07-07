from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

url = "https://cookidoo.de/recipes/recipe/de-DE/r620990"

driver = WebDriver()  # Initialize the Selenium WebDriver (make sure to have the appropriate driver installed)
try:
    driver.get(url)  # Open the URL in the browser
except Exception as e:
    print(f"Error accessing the URL: {e}")
    driver.quit()
    exit(1)

print("Loaded the recipe page successfully.")
print("Fetching recipe title and ingredients...")
try:
    recipe_name = driver.find_element("class name", "recipe-card__name").text
    print(f"Recipe name: {recipe_name}")
except Exception as e:
    print(f"Error fetching recipe name: {e}")
    driver.quit()
    exit(1)

try:
    ingredients = driver.find_elements(By.TAG_NAME, "recipe-ingredient")
    for ingredient in ingredients:
        print(f"Found ingredient: {ingredient.text}")
except Exception as e:
    print(f"Error fetching ingredients: {e}")
    driver.quit()
    exit(1)

# Close the driver after use
driver.quit()
exit(0)