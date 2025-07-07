import argparse
import yaml
import pathlib
from rich.console import Console
from libs.cookidoo_url_analyser import analyse_cookidoo_url

def main():

    if not pathlib.Path("output").exists():
        pathlib.Path("output").mkdir(parents=True)

    console = Console()
    console.print("Welcome to the Cookidoo Recipe Ingredient Extractor!", style="bold green")

    parser = argparse.ArgumentParser(description="A simple commend line tool to generate a yaml file with a list of ingredients and their quantities from a cookidoo recipe.")
    parser.add_argument("--recipe_url", type=str, help="The URL of the cookidoo recipe to extract ingredients from.", default=None, nargs="?")
    parser.add_argument("--recipe_html", type=str, help="The HTML file of the cookidoo recipe to extract ingredients from.", default=None, nargs="?")
    parser.add_argument("-o", "--output", type=str, help="The output YAML file to save the ingredients.", default=None)
    args = parser.parse_args()

    if not args.recipe_url and not args.recipe_html:
        console.print("Error: You must provide either a recipe URL or a recipe HTML file.", style="bold red")
        exit(1)

    if args.recipe_url:
        console.print(f"Analyzing Cookidoo URL: {args.recipe_url}", style="bold blue")
        recipe_data = analyse_cookidoo_url(args.recipe_url)
        if not recipe_data:
            console.print("Failed to retrieve recipe data. Please check the URL.", style="bold red")
            return 1
        
        yaml_data = yaml.dump(recipe_data, allow_unicode=True, sort_keys=False)
        if not args.output:
            args.output = pathlib.Path("output", recipe_data.get("name") + ".yaml")
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(yaml_data)
            console.print(f"Recipe ingredients saved to {args.output}", style="bold green")

    elif args.recipe_html:
        return 0


if __name__ == "__main__":
    main()