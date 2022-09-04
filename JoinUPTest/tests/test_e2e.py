from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from faker import Faker

from JoinUPTest.models import User, ActivationCode, ActivationCodeType
from django.conf import settings
from django.db import connection, reset_queries


@patch('JoinUPTest.models.User.email_user', return_value=None)
@patch('JoinUPTest.models.User.sms_user', return_value=None)
class UserTestCase(APITestCase):

    settings.DEBUG = True

    def setUp(self):
        faker = Faker('es_ES')
        self.password = faker.password(length=15, special_chars=False)
        self.fake_email = faker.email()
        self.fake_first_name = faker.first_name()
        self.fake_last_name = faker.last_name()
        self.fake_phone_number = faker.phone_number()
        self.fake_text = faker.text()

        self.data_register = {
            "email": self.fake_email,
            "password": self.password,
            "password2": self.password,
            "first_name": self.fake_first_name,
            "last_name": self.fake_last_name,
            "phone_number": self.fake_phone_number,
            "hobbies_description": self.fake_text,
        }
        self.data_login = {
            "username": self.fake_email,
            "password": self.password,
        }

    def test_signup(self, *args):
        reset_queries
        response = self.client.post(reverse("signup"), data=self.data_register, format='json')
        print(f"SIGNUP Access count DB :  {len(connection.queries)}")
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.data_register["email"], response.data["email"])
        self.assertEqual(self.data_register["first_name"], response.data["first_name"])
        self.assertEqual(self.data_register["last_name"], response.data["last_name"])
        self.assertEqual(self.data_register["phone_number"], response.data["phone_number"])
        self.assertEqual(self.data_register["hobbies_description"], response.data["hobbies_description"]),


    def test_login(self, *args):
        self.client.post(reverse("signup"), data=self.data_register, format='json')
        reset_queries
        response = self.client.post(reverse("login"), data=self.data_login, format='json')
        print(f"LOGIN Access count DB :  {len(connection.queries)}")
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(response.data["token"], "")

    def test_profile(self, *args):
        self.client.post(reverse("signup"), data=self.data_register, format='json')
        response = self.client.post(reverse("login"), data=self.data_login, format='json')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + response.data["token"])
        reset_queries
        response = client.get(reverse("profile"))
        print(f"PROFILE Access count DB :  {len(connection.queries)}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.data_register["email"], response.data["email"])
        self.assertEqual(self.data_register["first_name"], response.data["first_name"])
        self.assertEqual(self.data_register["last_name"], response.data["last_name"])
        self.assertEqual(self.data_register["phone_number"], response.data["phone_number"])
        self.assertEqual(response.data["email_validated"], False),
        self.assertEqual(response.data["phone_validated"], False),

    def test_activation(self, *args):
        self.client.post(reverse("signup"), data=self.data_register, format='json')
        response = self.client.post(reverse("login"), data=self.data_login, format='json')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + response.data["token"])

        response = client.get(reverse("profile"))
        self.assertEqual(response.data["email_validated"], False),
        self.assertEqual(response.data["phone_validated"], False),

        sms_activation_code = ActivationCode.objects.get(user_id=User.objects.get(email=self.fake_email), type=ActivationCodeType.SMS).code
        email_activation_code = ActivationCode.objects.get(user_id=User.objects.get(email=self.fake_email),
                                                      type=ActivationCodeType.EMAIL).code
        reset_queries
        self.client.get(reverse('activation', kwargs={"code": sms_activation_code}))
        print(f"ACTIVATION PHONE Access count DB :  {len(connection.queries)}")
        reset_queries
        self.client.get(reverse('activation', kwargs={"code": email_activation_code}))
        print(f"ACTIVATION EMAIL Access count DB :  {len(connection.queries)}")

        response = client.get(reverse("profile"))
        self.assertEqual(response.data["email_validated"], True),
        self.assertEqual(response.data["phone_validated"], True),




