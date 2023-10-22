import respx
import httpx

from fastapi.testclient import TestClient
from main import app
from src.services.first_fifty_comments import  HACKERNEWS_API

client = TestClient(app)

@respx.mock
def test_read_top_stories_comments():
    # Mock the /topstories.json endpoint to return a single story
    respx.get(f'{HACKERNEWS_API}/topstories.json').mock(return_value=httpx.Response(200, json=[1]))

    # Mock the /item/{story_id}.json endpoint to return a story with a single comment
    respx.get(f'{HACKERNEWS_API}/item/1.json').mock(return_value=httpx.Response(200, json={'kids': [100]}))

    # Mock the /item/{comment_id}.json endpoint to return a comment
    respx.get(f'{HACKERNEWS_API}/item/100.json').mock(return_value=httpx.Response(200, json={
        'id': 100,
        'text': 'Test comment',
        'by': 'test_user',
        'parent': 1,
        'time': 1634809123,
        'deleted': None,  # Add the deleted field
        'dead': None,  # Add the dead field
    }))

    response = client.get("/first_fifty_comments/")
    assert response.status_code == 200
    assert response.json() == [{
        'id': 100,
        'text': 'Test comment',
        'by': 'test_user',
        'parent': 1,
        'time': 1634809123,
        'deleted': None,  # Expect the deleted field in the response
        'dead': None,  # Expect the dead field in the response
    }]

@respx.mock
def test_read_top_stories_comments_api_unavailable():
    # Mock the /topstories.json endpoint to return an error status code
    respx.get(f'{HACKERNEWS_API}/topstories.json').mock(return_value=httpx.Response(500))

    response = client.get("/first_fifty_comments/")
    assert response.status_code == 500
