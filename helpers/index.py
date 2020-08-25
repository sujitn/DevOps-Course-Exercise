import logging
from datetime import datetime

from entity.item import Item
from trello_requests.lists import get_lists_on_board

log = logging.getLogger('app')

trello_date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def start_of_day(day):
    return day.replace(hour=0, minute=0, second=0, microsecond=0)


def map_trello_items(trello_lists, trello_items):
    items = []
    for trello_item in trello_items:
        for trello_list in trello_lists:
            if (trello_item.listId == trello_list.id):
                items.append(
                    Item(
                        trello_item.id,
                        trello_item.title,
                        trello_list.name,
                        trello_item.dateLastActivity
                    )
                )
                break
    return items


def get_id_of_list(name):
    log.debug(f'Getting list with name {name}')
    lists = get_lists_on_board()
    for list in lists:
        if(list.name == name):
            return list.id
    log.debug(f'No list found with name {name}')


def filter_items_by_list(items, list_name):
    filtered_items = []
    for item in items:
        if(item.status == list_name):
            filtered_items.append(item)
    return filtered_items


def filter_items_modified_today(items):
    start_of_today = start_of_day(datetime.now())

    filtered_items = []

    for item in items:
        modified_time = datetime.strptime(
            item.lastModifiedDate,
            trello_date_time_format
        )
        modified_date = start_of_day(modified_time)

        if(start_of_today == modified_date):
            filtered_items.append(item)

    return filtered_items


def filter_items_last_modified_before_today(items):
    start_of_today = start_of_day(datetime.now())

    filtered_items = []

    for item in items:
        modified_time = datetime.strptime(
            item.lastModifiedDate,
            trello_date_time_format
        )

        if(modified_time < start_of_today):
            filtered_items.append(item)

    return filtered_items
