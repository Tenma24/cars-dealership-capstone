import requests
from django.conf import settings

def get_request(endpoint):
    response=requests.get(settings.BACKEND_URL+'/'+endpoint.lstrip('/'),timeout=8)
    response.raise_for_status()
    return response.json()

def analyze_review_sentiments(text):
    response=requests.post(settings.SENTIMENT_URL+'/analyze',json={'text':text},timeout=8)
    response.raise_for_status()
    return response.json()

def post_review(data):
    response=requests.post(settings.BACKEND_URL+'/insert_review',json=data,headers={'X-Service-Token':settings.SERVICE_TOKEN},timeout=8)
    response.raise_for_status()
    return response.json()
