from unittest.mock import patch, Mock
from datetime import date, datetime, timedelta
import pytest
from dotenv import load_dotenv, find_dotenv
from item import Item
import app


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client


# @patch('app.get_db_collection')
@patch('app.get_items')
def test_index_page(get_items, client):

    get_items.side_effect = mock_get_items

    response = client.get('/')

    response_html = response.data.decode()

    assert 'Task 1' in response_html
    assert 'Task 2' in response_html
    assert 'Task 3' in response_html


def mock_get_items(collection):
    items = [
        Item(1, 'Done', 'Task 1', date.today()),
        Item(2, 'Doing', 'Task 2', date.today()),
        Item(3, 'ToDo', 'Task 3', date.today()),
    ]
    return items


def mock_get_db_collection():
    return
