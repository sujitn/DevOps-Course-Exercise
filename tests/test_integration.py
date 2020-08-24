from unittest.mock import patch, Mock
from datetime import date, datetime, timedelta
import pytest
from dotenv import load_dotenv, find_dotenv
from item import TrelloItem
import app


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client

@patch('app.get_items')
def test_index_page(get_items, client):
    get_items.side_effect = mock_get_items

    response = client.get('/')

    response_html = response.data.decode()
    assert 'Task 1' in response_html
    assert 'Task 2' in response_html
    assert 'Task 3' in response_html
    

def mock_get_items(api_key,token,board_id):
    items = [
        TrelloItem(1,'Done', 'Task 1', date.today()),
        TrelloItem(2,'Doing', 'Task 2', date.today()),
        TrelloItem(3,'ToDo', 'Task 3', date.today()),
    ]
    return items
    
def mock_get_lists(url, params):
    if url == 'https://api.trello.com/1/boards/abcd1234/lists':
        response = Mock(ok=True)
        response.json.return_value = sample_trello_lists_response
        return response

    return None
