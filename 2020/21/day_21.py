import sys
from collections import defaultdict
from typing import List, Tuple

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    # Crawl through the list of foods and build lots of lists.
    all_ingredients_set = set()
    all_ingredients_list = list()
    allergen_dict = defaultdict(list)
    food_list = parse_food(file=input_file)
    for ingredients, allergens in food_list:
        all_ingredients_list += ingredients
        for a in allergens:
            ingredient_set = set()
            for i in ingredients:
                all_ingredients_set.add(i)
                ingredient_set.add(i)
            allergen_dict[a].append(ingredient_set)

    # Build a dictionary of possible translations
    possible_translations = dict()
    for allergen, ingredient_sets in allergen_dict.items():
        set_a = ingredient_sets[0]  # type: set
        intersection = set_a.intersection(*ingredient_sets[1:])
        possible_translations[allergen] = intersection

    # Get all possible allergens
    possible_allergens = set()
    for value in possible_translations.values():
        possible_allergens.update(value)

    # Find the number of times non-contaminated ingredients appear (part 1)
    count = 0
    not_contaminated = all_ingredients_set.difference(possible_allergens)
    for ingredient in not_contaminated:
        count += all_ingredients_list.count(ingredient)
    print(f"Non-contaminated ingredients appear {count} times.")

    # Continue using known translations (where possibilities == 1) to narrow down the list of possible translations.
    while max(len(v) for v in possible_translations.values()) > 1:
        solved_translations = set()
        for value in possible_translations.values():
            if len(value) == 1:
                solved_translations.update(value)
        for key, value in possible_translations.items():
            if len(value) > 1:
                possible_translations[key].difference_update(solved_translations)

    # Print list of dangerous ingredients (part 2)
    dangerous_ingredients = []
    for key in sorted(possible_translations.keys()):
        dangerous_ingredients.append(min(possible_translations[key]))
    print("Canonical dangerous ingredient list:")
    print(",".join(dangerous_ingredients))

    return 0


def parse_food(file: str):
    food_list = []
    for line in read_lines(file_path=file):
        ingredients, allergens = line.split(" (contains ")
        food_list.append(([i.strip() for i in ingredients.split(" ")], [a.strip(" )") for a in allergens.split(", ")]))
    return food_list


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
