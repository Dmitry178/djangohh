from django.test import Client
from django.test import TestCase
from faker import Faker
from userapp.models import HhUser


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fake = Faker()

    def test_status_codes(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/region-list')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/contacts/',
                                    {'name': self.fake.name(),
                                     'email': self.fake.email(),
                                     'message': self.fake.text()})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertTrue('index_image' in response.context)

    def test_login_required(self):
        HhUser.objects.create_user(username='user', email='user@test.com', password='test_password')

        # неавторизованный вход
        response = self.client.get('/region-create/')
        self.assertEqual(response.status_code, 302)

        # вход авторизованного пользователя
        self.client.login(username='user', password='test_password')
        response = self.client.get('/region-create/')
        self.assertEqual(response.status_code, 200)

        # проверка входа авторизованного пользователя на страницу с доступом только для суперпользователя
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 302)
