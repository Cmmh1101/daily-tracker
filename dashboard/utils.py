from django.http import JsonResponse
import requests


def get_quote():
    url = 'https://zenquotes.io/api/random'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        return JsonResponse({'error': 'Failed to fetch quote'}, status=500)