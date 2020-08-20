import json
import os
from trello_requests.make_trello_request import make_trello_request
from trello_requests.helpers import extract_trello_list
from entity.http_method import HttpMethod
from entity.trello_list import TrelloList


def get_lists_on_board():
    endpoint = f'{os.getenv("TRELLO_API_BASE_URL")}/boards/{os.getenv("TRELLO_BOARD_ID")}/lists'
    method = HttpMethod.Get

    response = make_trello_request(method, endpoint)
    return list(map(extract_trello_list, response.json()))


def create_list(list_name):
    endpoint = f'{os.getenv("TRELLO_API_BASE_URL")}/lists'
    params = {'name': list_name, 'idBoard': os.getenv("TRELLO_BOARD_ID")}
    method = HttpMethod.Post

    response = make_trello_request(method, endpoint, params)
    return response.json()['id']
