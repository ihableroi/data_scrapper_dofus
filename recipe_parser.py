def parse_recipes(input_file, output_file):
    try:
        # Try to read with UTF-8 encoding
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except UnicodeDecodeError:
        # Fallback to ISO-8859-1 encoding if UTF-8 fails
        with open(input_file, 'r', encoding='ISO-8859-1') as infile:
            lines = infile.readlines()

    formatted_recipes = []

    for line in lines:
        # Split recipe into name and ingredients
        if '=' in line:
            name, ingredients = line.strip().split('=', 1)
            name = name.strip("[]")  # Remove square brackets from the name
            
            # Process the ingredients
            ingredients_list = ingredients.split('+')
            parsed_ingredients = []
            
            for item in ingredients_list:
                count, ingredient = item.split('x', 1)
                count = count.strip()
                ingredient = ingredient.strip("[]").strip()
                parsed_ingredients.append(f"{ingredient};{count}")

            # Join the recipe name with parsed ingredients
            formatted_recipe = f"{name}; " + "; ".join(parsed_ingredients) + ";"
            formatted_recipes.append(formatted_recipe)

    # Write formatted recipes to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(formatted_recipes))

# Example usage
input_file = "recettes_marteaux.txt"  # Replace with your input file path
output_file = "formatted_recettes_marteaux.csv"  # Replace with your desired output file path
parse_recipes(input_file, output_file)
