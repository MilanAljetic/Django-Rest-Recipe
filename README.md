# Django-Rest-Recipe
Django web service for Food recipes


## Instalation
- python3 -m venv venv
- source .venv/bin/activate
- pip3 install -r requirements.txt
- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py runserver


## ENDPOINTS

### - User endpoints

/api/user/login/ - Login and get JWT token

/api/user/register/ - Register user

/api/user/token/refresh/ - Refresh token

/api/user/int:pk/ - Get user info

### - Recipes endpoints

/api/recipes/ - List of all recipes

/api/recipes/user/ - List of own recipes

/api/ingredients/ - List/Create ingredients

/api/recipes/create/ - Create recipe

/api/recipes/rate/ - Rate recipe

/api/recipes/?search=STRING - Search recipes (name, text, ingredient)

/api/recipes/?max_ing_num=INT - Recipes with maximum numbers of ingredients

/api/recipes/?min_ing_num=INT - Recipes with minimum numbers of ingredients

### - Testing

- python3 manage.py test
