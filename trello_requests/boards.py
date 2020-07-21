import json
import consts

from trello_requests.make_trello_request import make_trello_request
from entity.http_method import HttpMethod


def create_board(name):
    endpoint = f'{consts.trello_base_url}/boards'
    params = {'name': name}
    method = HttpMethod.Post

    response = make_trello_request(method, endpoint, params)
    return response.json()['id']


def delete_board(board_id):
    endpoint = f'{consts.trello_base_url}/{board_id}'
    method = HttpMethod.Delete

    make_trello_request(method, endpoint, params)
