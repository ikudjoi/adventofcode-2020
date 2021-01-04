import os
import math

script_file = os.path.basename(__file__)
input_file = os.path.join('input', script_file.replace('.py', '.txt'))
with open(input_file) as f:
    content = f.read()

train_content = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
#content = train_content

raw_recipes = content.splitlines()
allergens_to_ingredients = {}
recipes = []
for recipe in raw_recipes:
    ingredients, allergens = recipe.split(' (contains ')
    ingredients = set(ingredients.split(' '))
    allergens = set(allergens[:-1].split(', '))
    recipes.append([ingredients, allergens])
    for allergen in allergens:
        if allergen not in allergens_to_ingredients:
            allergens_to_ingredients[allergen] = ingredients
        else:
            allergens_to_ingredients[allergen] = allergens_to_ingredients[allergen] & ingredients

all_possible_allergens = set()
for allergen_ingredients in allergens_to_ingredients.values():
    all_possible_allergens = all_possible_allergens.union(allergen_ingredients)

# part 1
cnt_non_allergens = 0
for ingredients, _ in recipes:
    non_allergens_in_recipe = ingredients - all_possible_allergens
    cnt_non_allergens += len(non_allergens_in_recipe)
print(cnt_non_allergens)

determined_allergens = []
while any([i for i in allergens_to_ingredients.values() if len(i) > 1]):
    all_allergens = list(allergens_to_ingredients.values())

    unambiguous_allergens = [next(iter(allergens)) for allergens in all_allergens if len(allergens) == 1 and next(iter(allergens)) not in determined_allergens]
    for allergen in unambiguous_allergens:
        for ingredients in allergens_to_ingredients.values():
            if len(ingredients) == 1:
                continue
            if allergen in ingredients:
                ingredients.remove(allergen)
                if not allergen in determined_allergens:
                    determined_allergens.append(allergen)
allergens_to_ingredients = {allergen: ingredient.pop() for allergen, ingredient in sorted(allergens_to_ingredients.items())}
print(",".join(allergens_to_ingredients.values()))
