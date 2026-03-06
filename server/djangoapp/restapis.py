import requests
import os
from dotenv import load_dotenv

# Prioritize Kubernetes environment variables
backend_url = os.environ.get('backend_url', "http://localhost:3030")
sentiment_analyzer_url = os.environ.get(
    'sentiment_analyzer_url',
    "http://localhost:5050/"
)

# Only load .env if not in a containerized environment (optional fallback)
if not os.environ.get('KUBERNETES_SERVICE_HOST'):
    _base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _env_path = os.path.join(_base_dir, '.env')
    if os.path.exists(_env_path):
        load_dotenv(_env_path)
        # Re-check after loading .env if they weren't set
        if backend_url == "http://localhost:3030":
            backend_url = os.getenv('backend_url', backend_url)
        if sentiment_analyzer_url == "http://localhost:5050/":
            sentiment_analyzer_url = os.getenv(
                'sentiment_analyzer_url',
                sentiment_analyzer_url
            )


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"

    request_url = backend_url + endpoint + "?" + params

    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
