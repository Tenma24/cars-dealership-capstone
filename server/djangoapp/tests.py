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

    def test_validation_errors(self):
        data = {'userName':'x','firstName':'Alex','lastName':'Smith','email':'invalid','password':'password'}
        self.assertEqual(self.client.post('/djangoapp/register',data,content_type='application/json').status_code,400)
        data['email']='alex@example.com'
        self.assertEqual(self.client.post('/djangoapp/register',data,content_type='application/json').status_code,400)


class DealerTests(TestCase):
    def setUp(self):
        from .models import CarMake, CarModel
        self.make=CarMake.objects.create(name='Audi')
        self.model=CarModel.objects.create(car_make=self.make,name='A4',type='Sedan',year=2023)
        self.user=User.objects.create_user('driver',first_name='Alex',last_name='Morgan')
        self.client.force_login(self.user)

    @patch('djangoapp.views.get_request')
    def test_dealer_queries(self,get):
        get.return_value=[{'id':1,'state':'Kansas'}]
        self.assertEqual(self.client.get('/djangoapp/get_dealers').json()['dealers'][0]['id'],1)
        self.client.get('/djangoapp/get_dealers/Kansas')
        get.assert_called_with('fetchDealers/Kansas')
        get.return_value={'id':1}
        self.assertEqual(self.client.get('/djangoapp/dealer/1').json()['dealer']['id'],1)
        get.return_value=None
        self.assertEqual(self.client.get('/djangoapp/dealer/99999').status_code,404)

    @patch('djangoapp.views.analyze_review_sentiments',return_value={'sentiment':'positive'})
    @patch('djangoapp.views.get_request',return_value=[{'id':1,'review':'Fantastic services'}])
    def test_review_sentiments(self,get,analyze):
        self.assertEqual(self.client.get('/djangoapp/reviews/dealer/1').json()['reviews'][0]['sentiment'],'positive')

    @patch('djangoapp.views.get_request')
    def test_service_failure(self,get):
        import requests
        get.side_effect=requests.ConnectionError()
        self.assertEqual(self.client.get('/djangoapp/get_dealers').status_code,503)

    @patch('djangoapp.views.post_review',side_effect=lambda data:data)
    @patch('djangoapp.views.analyze_review_sentiments',return_value={'sentiment':'positive'})
    @patch('djangoapp.views.get_request',return_value={'id':1})
    def test_add_review_and_validation(self,get,analyze,post):
        data={'dealership':1,'review':'Fantastic services','purchase':True,'car_model_id':self.model.id,'purchase_date':'2020-01-02','name':'FORGED NAME'}
        response=self.client.post('/djangoapp/add_review',data,content_type='application/json')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json()['review']['name'],'Alex Morgan')
        self.assertEqual(response.json()['review']['car_make'],'Audi')
        for key,value in [('dealership','1'),('review',''),('purchase','yes'),('car_model_id',99999),('purchase_date','2999-01-01')]:
            self.assertEqual(self.client.post('/djangoapp/add_review',{**data,key:value},content_type='application/json').status_code,400)
        self.assertEqual(self.client.post('/djangoapp/add_review',{'dealership':1,'review':'Great','purchase':False},content_type='application/json').status_code,201)
        get.return_value=None
        self.assertEqual(self.client.post('/djangoapp/add_review',data,content_type='application/json').status_code,404)

    def test_models_and_catalog(self):
        self.assertEqual(str(self.make),'Audi')
        self.assertEqual(str(self.model),'Audi A4 (2023)')
        self.assertEqual(self.client.get('/djangoapp/get_cars').json()['car_makes'][0]['models'][0]['year'],2023)

    @patch('djangoapp.restapis.requests.get')
    @patch('djangoapp.restapis.requests.post')
    def test_service_client(self,post,get):
        from .restapis import get_request,post_review,analyze_review_sentiments
        get.return_value.json.return_value=[]
        post.return_value.json.return_value={'sentiment':'positive'}
        self.assertEqual(get_request('fetchDealers'),[])
        self.assertEqual(analyze_review_sentiments('great')['sentiment'],'positive')
        self.assertEqual(post_review({'review':'great'})['sentiment'],'positive')
