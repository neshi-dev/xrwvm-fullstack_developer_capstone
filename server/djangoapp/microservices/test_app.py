"""
Unit tests for the Flask sentiment analyser microservice (app.py).

Run with:
    python -m pytest test_app.py -v
"""
import json
import pytest
from app import app


@pytest.fixture
def client():
    """Return a Flask test client with testing mode enabled."""
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


class TestHomeEndpoint:
    def test_home_returns_200(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_home_contains_welcome_message(self, client):
        response = client.get('/')
        assert b'Welcome' in response.data


class TestAnalyseSentimentEndpoint:
    def _analyse(self, client, text):
        response = client.get(f'/analyze/{text}')
        assert response.status_code == 200
        return json.loads(response.data)

    def test_positive_review_classified_as_positive(self, client):
        text = 'This%20car%20is%20absolutely%20fantastic%20and%20wonderful'
        data = self._analyse(client, text)
        assert data['sentiment'] == 'positive'

    def test_negative_review_classified_as_negative(self, client):
        text = 'Terrible%20awful%20horrible%20worst%20experience%20ever'
        data = self._analyse(client, text)
        assert data['sentiment'] == 'negative'

    def test_neutral_review_classified_as_neutral(self, client):
        data = self._analyse(client, 'The%20car%20exists')
        assert data['sentiment'] == 'neutral'

    def test_response_contains_sentiment_key(self, client):
        data = self._analyse(client, 'okay')
        assert 'sentiment' in data

    def test_sentiment_value_is_one_of_valid_options(self, client):
        data = self._analyse(client, 'It%20was%20alright')
        assert data['sentiment'] in ('positive', 'negative', 'neutral')

    def test_empty_text_returns_200(self, client):
        response = client.get('/analyze/ ')
        assert response.status_code == 200
