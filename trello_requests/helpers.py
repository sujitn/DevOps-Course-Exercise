from entity.trello_card import TrelloCard
from entity.trello_list import TrelloList


def extract_trello_list(response_item):
    return TrelloList(response_item['id'], response_item['name'])


def extract_trello_item(response_item):
    return TrelloCard(response_item['id'], response_item['name'], response_item['idList'], response_item['dateLastActivity'])
