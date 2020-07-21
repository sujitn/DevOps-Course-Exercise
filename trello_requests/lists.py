import json
import consts
from trello_requests.make_trello_request import make_trello_request
from trello_requests.helpers import extract_trello_list
from entity.http_method import HttpMethod
from entity.trello_list import TrelloList


def get_lists_on_board():
    endpoint = f'{consts.trello_base_url}/boards/{consts.trello_board_id}/lists'
    method = HttpMethod.Get

    response = make_trello_request(method, endpoint)
    return list(map(extract_trello_list, response.json()))
