import requests
from bs4 import BeautifulSoup


def get_recipe_ingredients(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ingredients = soup.select("ul.ingredient-lists.css-xm7ys2.eno1xhi3 li")
    ingredients_list = []
    for ingredient in ingredients:
        ingredients_list.append(ingredient.text.lower())
    return ingredients_list


response = requests.get("https://www.delish.com/uk/cooking/recipes/")
soup = BeautifulSoup(response.text, 'html.parser')

base_url = "https://www.delish.com"
found_first_url = False

urls = []
error = True

for link in soup.find_all('a', {'data-vars-ga-outbound-link': True}):
    url = link.get('href')
    if not found_first_url:
        found_first_url = True
        continue
    full_url = base_url + url
    urls.append(full_url)

user_input = input("Enter your ingredients (comma-separated): ").lower()
user_ingredients = [ingredient.strip() for ingredient in user_input.split(",")]

for one_link in urls:
    recipe_ingredients = get_recipe_ingredients(one_link)

    matching_ingredients = []
    for ingredient in user_ingredients:
        for recipe in recipe_ingredients:
            if ingredient in recipe:
                matching_ingredients.append(ingredient)

    if matching_ingredients:
        error = False

        response = requests.get(one_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        names = soup.select("h1.css-2l10x9.exadjwu10")
        method = soup.select("li.css-12948jm.evb48wp3 li")
        get_link = soup.select("link")

        for name in names:
            print(f"\n{name.text}\n")

        print("Ingredients: ")
        for item in recipe_ingredients:
            print(f"{item}\n")

        print("Methods: ")
        for step in method:
            print(f"\n{step.text}\n")

        print("Url: ")
        print(get_link[0]['href'])

if error:
    print(
        f"One of these ingredients or more not found! \n{user_ingredients}")
