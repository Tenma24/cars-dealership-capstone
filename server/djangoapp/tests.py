import json
from unittest.mock import patch
from django.test import TestCase, Client
from django.contrib.auth.models import User


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('driver', password='RoadTrip!73921')

    def test_login_logout_session(self):
        response = self.client.post('/djangoapp/login', json.dumps({'userName': 'driver', 'password': 'RoadTrip!73921'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Authenticated')
        self.assertEqual(self.client.get('/djangoapp/session').json()['userName'], 'driver')
        self.assertEqual(self.client.post('/djangoapp/logout').status_code, 200)
        self.assertIsNone(self.client.get('/djangoapp/session').json()['userName'])

    def test_invalid_login(self):
        response = self.client.post('/djangoapp/login', {'userName': 'driver', 'password': 'wrong'}, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_register_and_duplicate(self):
        data = {'userName': 'newdriver', 'firstName': 'Alex', 'lastName': 'Smith', 'email': 'alex@example.com', 'password': 'RoadTrip!73921'}
        self.assertEqual(self.client.post('/djangoapp/register', data, content_type='application/json').status_code, 201)
        self.assertEqual(self.client.post('/djangoapp/register', data, content_type='application/json').status_code, 400)
        self.assertTrue(User.objects.get(username='newdriver').check_password(data['password']))

    def test_bad_input(self):
        for body in ['{', '[]', '{}', '{"userName":1}']:
            self.assertEqual(self.client.post('/djangoapp/register', body, content_type='application/json').status_code, 400)

    def test_csrf_enforced(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/djangoapp/login', {}, content_type='application/json').status_code, 403)

    def test_review_requires_login(self):
        self.assertEqual(self.client.post('/djangoapp/add_review', {}, content_type='application/json').status_code, 401)

    def test_cars(self):
        self.assertEqual(self.client.get('/djangoapp/get_cars').status_code, 200)

    def test_readonly_login(self):
        self.assertEqual(self.client.get('/djangoapp/login').status_code, 405)
