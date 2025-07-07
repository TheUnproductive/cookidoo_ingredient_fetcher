import yaml
from pathlib import Path

def create_yaml(recipe: dict, output_path: Path = None) -> None:
    yaml_data = yaml.dump(recipe, allow_unicode=True, sort_keys=False)
    if output_path is None:
        output_path = Path("output", recipe.get("name") + ".yaml")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(yaml_data)
