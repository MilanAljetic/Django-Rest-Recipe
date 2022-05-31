import clearbit
import requests
from django.conf import settings
from rest_framework import serializers, status


def hunter_verify(email):
    api_key = settings.HUNTER_API_KEY
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code != status.HTTP_200_OK:
        raise serializers.ValidationError(f"Check mail error {response.status_code}")
    response_status = response.json()['data']['status']
    if response_status == 'invalid' or response_status == "disposable":
        return False
    return True


def clearbit_info(email):
    clearbit.key = settings.CLEARBIT_API_KEY
    response = clearbit.Enrichment.find(email=email, stream=True)
    if response is not None:
        return response
    else:
        return "Email hasn't additional information"
