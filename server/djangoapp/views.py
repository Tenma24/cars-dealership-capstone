import json
from datetime import date
from functools import wraps
from urllib.parse import quote
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import CarMake, CarModel
from .restapis import get_request, post_review, analyze_review_sentiments

def guarded(view):
    @wraps(view)
    def wrapper(request,*args,**kwargs):
        try:
            return view(request,*args,**kwargs)
        except (ValueError, TypeError, KeyError, ValidationError, IntegrityError):
            return JsonResponse({'error':'Invalid or duplicate input. Check all fields.'},status=400)
        except requests.RequestException:
            return JsonResponse({'error':'A service is unavailable. Please try again.'},status=503)
    return wrapper

def body(request):
    data=json.loads(request.body)
    if not isinstance(data,dict):
        raise ValueError('Expected object')
    return data

def text(data,key,limit=150):
    value=data.get(key)
    if not isinstance(value,str) or not value.strip() or len(value)>limit:
        raise ValueError(key)
    return value.strip()

@require_GET
def session(request):
    return JsonResponse({'userName':request.user.username if request.user.is_authenticated else None,'csrfToken':get_token(request)})

@require_POST
@guarded
def login_user(request):
    data=body(request)
    user=authenticate(request,username=text(data,'userName'),password=text(data,'password',128))
    if user is None:
        return JsonResponse({'error':'Invalid username or password.'},status=401)
    login(request,user)
    return JsonResponse({'userName':user.username,'status':'Authenticated','csrfToken':get_token(request)})

@require_http_methods(['GET','POST'])
def logout_request(request):
    # Course curl compatibility. The custom header prevents cross-origin
    # navigations/images from logging users out; do not enable credentialed CORS.
    # The browser UI continues to use a CSRF-protected POST.
    if request.method == 'GET' and request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error':'Use POST, or the course AJAX GET request.'},status=405)
    logout(request)
    return JsonResponse({'userName':'','status':'Logged out','csrfToken':get_token(request)})

@require_POST
@guarded
def registration(request):
    data=body(request)
    user=User(username=text(data,'userName'),first_name=text(data,'firstName'),last_name=text(data,'lastName'),email=text(data,'email',254))
    validate_email(user.email)
    user.full_clean(exclude=['password'])
    password=text(data,'password',128)
    validate_password(password,user)
    user.set_password(password)
    user.save()
    login(request,user)
    return JsonResponse({'userName':user.username,'status':'Authenticated','csrfToken':get_token(request)},status=201)

@require_GET
@guarded
def get_dealerships(request,state=None):
    endpoint='fetchDealers'+('/'+quote(state,safe='') if state else '')
    return JsonResponse({'dealers':get_request(endpoint)})

@require_GET
@guarded
def get_dealer_details(request,dealer_id):
    dealer=get_request('fetchDealer/'+str(dealer_id))
    return JsonResponse({'dealer':dealer}) if dealer else JsonResponse({'error':'Dealer not found'},status=404)

@require_GET
@guarded
def get_dealer_reviews(request,dealer_id):
    reviews=get_request('fetchReviews/dealer/'+str(dealer_id))
    for review in reviews:
        if 'sentiment' not in review:
            review['sentiment']=analyze_review_sentiments(review['review'])['sentiment']
    return JsonResponse({'reviews':reviews})

@require_GET
def get_cars(request):
    if request.GET.get('format') != 'grouped':
        cars = CarModel.objects.select_related('car_make').order_by('id')
        return JsonResponse({'CarModels': [
            {'CarModel': car.name, 'CarMake': car.car_make.name} for car in cars
        ]})
    return JsonResponse({'car_makes':[{'id':make.id,'name':make.name,'models':list(make.models.values('id','name','type','year'))} for make in CarMake.objects.prefetch_related('models').order_by('name')]})

@require_POST
@guarded
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error':'Please log in to post a review.'},status=401)
    data=body(request)
    dealer_id=data.get('dealership')
    if type(dealer_id) is not int or dealer_id<1:
        raise ValueError('Dealer')
    if not get_request('fetchDealer/'+str(dealer_id)):
        return JsonResponse({'error':'Dealer not found'},status=404)
    review=text(data,'review',2000)
    purchase=data.get('purchase',False)
    if type(purchase) is not bool:
        raise ValueError('Purchase')
    result={'dealership':dealer_id,'review':review,'purchase':purchase,'name':request.user.get_full_name() or request.user.username,'username':request.user.username}
    if purchase:
        model=CarModel.objects.filter(id=data.get('car_model_id')).select_related('car_make').first()
        if not model:
            raise ValueError('Car')
        purchase_date=date.fromisoformat(text(data,'purchase_date',10))
        if purchase_date>date.today():
            raise ValueError('Future date')
        result.update(car_make=model.car_make.name,car_model=model.name,car_year=model.year,purchase_date=str(purchase_date))
    result['sentiment']=analyze_review_sentiments(review)['sentiment']
    return JsonResponse({'review':post_review(result)},status=201)
