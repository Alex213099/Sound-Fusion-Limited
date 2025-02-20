import requests
import base64
import os
from django.conf import settings

def get_access_token():
    url = f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {"Authorization": f"Basic {encoded_credentials}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None
