from dotenv import find_dotenv, load_dotenv
import pytest
import json

from app import create_app
from entity.trello_list import TrelloList
from entity.trello_card import TrelloCard


@pytest.fixture
def client():
    file_path = find_dotenv('test_env_file.txt')
    load_dotenv(file_path, override=True)

    test_app = create_app()

    with test_app.test_client() as client:
        yield client


def stub_get_lists_on_board():
    return [
        TrelloList('test-to-do-list-id', 'To do'),
        TrelloList('test-doing-list-id', 'Doing'),
        TrelloList('test-done-list-id', 'Done')
    ]


def stub_get_items_on_board():
    return [
        TrelloCard(
            'test-to-do-card-id',
            'Test To Do Card Title',
            'test-to-do-list-id',
            '2020-06-24T14:51:12.321Z'
        ),
        TrelloCard(
            'test-doing-card-id',
            'Test Doing Card Title',
            'test-doing-list-id',
            '2020-06-24T14:51:12.321Z'
        ),
        TrelloCard(
            'test-done-card-id',
            'Test Done Card Title',
            'test-done-list-id',
            '2020-06-24T14:51:12.321Z'
        ),
    ]


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(
        'trello_requests.lists.get_lists_on_board.__code__',
        stub_get_lists_on_board.__code__
    )
    monkeypatch.setattr(
        'trello_requests.items.get_items_on_board.__code__',
        stub_get_items_on_board.__code__
    )

    response = client.get('/')

    content = response.data.decode('utf8')
    assert response.status_code == 200
    assert 'Test To Do Card Title' in content
    assert 'Test Doing Card Title' in content
    assert 'Test Done Card Title' in content
