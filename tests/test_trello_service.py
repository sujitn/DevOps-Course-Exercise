from unittest.mock import ANY, Mock, patch

from trello_items import get_lists

TRELLO_BASE_URL = ''
TRELLO_BOARD_ID = 'board-id'
TRELLO_API_KEY = 'api-key'
TRELLO_API_SECRET = 'api-secret'

@patch('trello_items.config')
@patch('trello_items.requests.get')
def test_get_lists(mock_get, mock_config):
    # Arrange
    setup_mock_config(mock_config)

    expected_response = get_default_trello_lists_response()
    expected_url = get_expected_url_with_path('/boards/' + TRELLO_BOARD_ID + '/lists')

    # Configure the mock to return a response with an OK status and JSON return value.
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = expected_response

    # Act
    response = get_lists()

    # Assert
    assert response == expected_response
    mock_get.assert_called_once_with(expected_url, params = ANY)

def setup_mock_config(mock_config):
    mock_config.TRELLO_BASE_URL = TRELLO_BASE_URL
    mock_config.TRELLO_BOARD_ID = TRELLO_BOARD_ID
    mock_config.TRELLO_API_KEY = TRELLO_API_KEY
    mock_config.TRELLO_API_SECRET = TRELLO_API_SECRET

def get_expected_url_with_path(path):
    return TRELLO_BASE_URL + path

def get_default_trello_lists_response():
    return [
        {
            'name': 'To Do',
            'id': '5e4a86ad89d1306c8897c022',
            'idBoard': '5e4a86ad89d1306c8897c021',
            'closed': False,
            'cards': [
                {
                    'name': 'New item',
                    'id': '5e553cc3085ee27e06236c66',
                    'dateLastActivity': '2020-03-03T12:34:56.789Z',
                    'idBoard': '5e4a86ad89d1306c8897c021',
                    'idList': '5e4a86ad89d1306c8897c022',
                    'closed': False
                }
            ]
        },
        {
            'name': 'Doing',
            'id': '5e4a86ad89d1306c8897c023',
            'idBoard': '5e4a86ad89d1306c8897c021',
            'closed': False,
            'cards': [
                {
                    'name': 'In-progress item',
                    'id': '5e55535c45315677e0cd2f94',
                    'dateLastActivity': '2020-02-02T12:34:56.789Z',
                    'idBoard': '5e4a86ad89d1306c8897c021',
                    'idList': '5e4a86ad89d1306c8897c023',
                    'closed': False
                }
            ]
        },
        {
            'name': 'Done',
            'id': '5e4a86ad89d1306c8897c024',
            'idBoard': '5e4a86ad89d1306c8897c021',
            'closed': False,
            'cards': [
                {
                    'name': 'Completed item',
                    'id': '5e7e0503e9d4c2774f25d0fd',
                    'dateLastActivity': '2020-01-01T12:34:56.789Z',
                    'idBoard': '5e4a86ad89d1306c8897c021',
                    'idList': '5e4a86ad89d1306c8897c024',
                    'closed': False
                }
            ]
        }
    ]
