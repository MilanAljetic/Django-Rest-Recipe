import json

from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from recipe.models import Ingredient, Recipe
from user.models import User

fake = Faker()


class TestUserAPIView(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="fake123@mail.com",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        self.password = "djangotest123"
        self.user.set_password(self.password)
        self.user.save()

        token = self.test_user_login()['access']
        self.header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}

        self.ingredients = Ingredient.objects.create(
            name="Milk"
        )

        self.recipe = Recipe.objects.create(
            author=self.user,
            name="Pizza",
            text="pizza italiano",
        )

    def test_user_register(self):
        url = reverse("user_register")

        data = {
            "email": "fake@fake.com",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": "fake1234"
        }
        data_json = json.dumps(data)
        response_post = self.client.post(url, data_json, content_type="application/json")
        response_data = json.loads(response_post.content)

        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(data['email'], response_data['email'])

        return response_data

    def test_user_login(self):
        url = reverse("user_login")

        data = {
            "email": self.user.email,
            "password": self.password
        }
        data_json = json.dumps(data)
        response_post = self.client.post(url, data_json, content_type="application/json")
        response_data = json.loads(response_post.content)

        self.assertEqual(response_post.status_code, 200)
        self.assertIn('refresh', response_data)

        return response_data

    def test_token_refresh(self):
        url = reverse("token_refresh")

        data = {
            "refresh": self.test_user_login()['refresh'],
        }
        data_json = json.dumps(data)
        response_post = self.client.post(url, data_json, content_type="application/json")
        response_data = json.loads(response_post.content)

        self.assertEqual(response_post.status_code, 200)
        self.assertIn('access', response_data)

    def test_user_info(self):
        url = reverse('user_info', args=[self.user.id])
        response = self.client.get(url, {}, **self.header, follow=True)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.email, response_data['email'])

    def test_ingredients(self):
        url = reverse('ingredients')

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.ingredients.name, response_data[0]['name'])

    def test_create_recipes(self):
        url = reverse("create_recipes")

        data = {
            "name": "Pizza",
            "text": "New Pizza",
            "ingredient": [self.ingredients.id]
        }
        data_json = json.dumps(data)
        response_post = self.client.post(url, data_json, content_type="application/json", **self.header, follow=True)
        response_data = json.loads(response_post.content)

        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(response_data['name'], data['name'])

    def test_all_recipes(self):
        url = reverse('all_recipes')

        response = self.client.get(url, {}, **self.header, follow=True)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.recipe.name, response_data[0]['name'])

    def test_user_recipes(self):
        url = reverse('user_recipes')

        response = self.client.get(url, {}, **self.header, follow=True)

        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.id, response_data[0]['author'])

    def test_rate(self):
        url = reverse("rate")

        user = User.objects.create(
            email="fake@mail.com",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password="pass123"
        )

        recipe = Recipe.objects.create(
            author=user,
            name="Pizza",
            text="pizza italiano",
        )

        # rate of someone else's recipe
        data = {
            "recipe": recipe.id,
            "rate": 4
        }
        data_json = json.dumps(data)
        response_post = self.client.post(url, data_json, content_type="application/json", **self.header, follow=True)
        response_data = json.loads(response_post.content)

        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(response_data['rate'], data['rate'])

        # rate of own recipe
        data = {
            "recipe": self.recipe.id,
            "rate": 4
        }
        data_json = json.dumps(data)
        response_post = self.client.post(url, data_json, content_type="application/json", **self.header, follow=True)
        response_data = json.loads(response_post.content)

        self.assertEqual(response_post.status_code, 400)
        self.assertEqual(response_data[0], "Can't rate your recipe!")
