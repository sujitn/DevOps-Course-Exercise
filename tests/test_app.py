from flask import request, url_for
from unittest.mock import ANY, Mock, patch
from todo_item import Item

import pytest

import app

@pytest.fixture
def client():
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        yield client

@patch('trello_items.get_items')
def test_index_page_displays_app_title(mock_get_items, client):
    # Arrange
    mock_get_items.return_value = []
    # Act
    response = client.get('/')
    # Assert
    assert b'To-Do App' in response.data

@patch('trello_items.get_items')
def test_index_page_lists_todo_items(mock_get_items, client):
    # Arrange
    item = Item('1', 'Integration test item')
    mock_get_items.return_value = [item]
    # Act
    response = client.get('/')
    # Assert
    response_html = response.data.decode()
    assert item.name in response_html
    assert item.status in response_html
    assert 'Start' in response_html

@patch('trello_items.get_items')
def test_index_page_lists_started_items(mock_get_items, client):
    # Arrange
    item = Item('1', 'Integration test item')
    item.start()
    mock_get_items.return_value = [item]
    # Act
    response = client.get('/')
    # Assert
    response_html = response.data.decode()
    assert item.name in response_html
    assert item.status in response_html
    assert 'Complete' in response_html

@patch('trello_items.get_items')
def test_index_page_lists_completed_items(mock_get_items, client):
    # Arrange
    item = Item('1', 'Integration test item')
    item.complete()
    mock_get_items.return_value = [item]
    # Act
    response = client.get('/')
    # Assert
    response_html = response.data.decode()
    assert item.name in response_html
    assert item.status in response_html
    assert 'Mark as Incomplete' in response_html

@patch('trello_items.add_item')
@patch('trello_items.get_items')
def test_add_item_creates_new_item(mock_get_items, mock_add_item, client):
    # Arrange
    item = Item('1', 'Integration test item')
    form_data = dict(name = item.name)
    # Act
    response = client.post('/items/new', data = form_data, follow_redirects = True)
    # Assert
    mock_add_item.assert_called_once_with(item.name)

@patch('trello_items.add_item')
@patch('trello_items.get_items')
def test_add_item_redirects_to_index_page(mock_get_items, mock_add_item, client):
    # Arrange
    item = Item('1', 'Integration test item')
    mock_get_items.return_value = [item]
    form_data = dict(name = item.name)
    # Act
    response = client.post('/items/new', data = form_data, follow_redirects = True)
    # Assert
    assert request.path == url_for('index')
    assert item.name in response.data.decode()
