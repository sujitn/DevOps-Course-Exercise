from dotenv import find_dotenv, load_dotenv
import pytest
import json

from app import create_app
from entity.trello_list import TrelloList
from entity.trello_card import TrelloCard

import consts


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = create_app()

    with test_app.test_client() as client:
        yield client


def stub_get_lists_on_board():
    return [TrelloList('test-list-id', 'test-name')]


def stub_get_items_on_board():
    return [TrelloCard('test-title', 'test-title','test-list-id', '2020-06-24T14:51:12.321Z')]


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(
        'trello_requests.index.get_lists_on_board.__code__',
        stub_get_lists_on_board.__code__
    )
    monkeypatch.setattr(
        'trello_requests.index.get_items_on_board.__code__',
        stub_get_items_on_board.__code__
    )

    response = client.get('/')

    assert response.status_code == 200
