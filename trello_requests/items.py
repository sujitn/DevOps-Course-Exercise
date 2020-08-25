import json
import os
from trello_requests.make_trello_request import make_trello_request
from trello_requests.helpers import extract_trello_item
from entity.http_method import HttpMethod
from entity.trello_card import TrelloCard


def get_items_on_board():
    endpoint = f'{os.getenv("TRELLO_API_BASE_URL")}/boards/{os.getenv("TRELLO_BOARD_ID")}/cards'
    method = HttpMethod.Get

    response = make_trello_request(method, endpoint)
    return list(map(extract_trello_item, response.json()))


def update_item_list(item_id, list_id):
    endpoint = f'{os.getenv("TRELLO_API_BASE_URL")}/cards/{item_id}'
    params = {
        'idList': list_id
    }
    method = HttpMethod.Put

    make_trello_request(method, endpoint, params)


def create_item(item_name, list_id):
    endpoint = f'{os.getenv("TRELLO_API_BASE_URL")}/cards'
    params = {
        'name': item_name,
        'idList': list_id
    }
    method = HttpMethod.Post

    make_trello_request(method, endpoint, params)
