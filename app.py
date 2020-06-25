import os
import json
from flask import Flask, render_template, request, redirect, url_for
import requests

from entity.trello_list import TrelloList 
from entity.trello_card import TrelloCard
from entity.item import Item
from entity.http_method import HttpMethod
from entity.list_name import ListName

trello_base_url = os.getenv('TRELLO_API_BASE_URL')
trello_key = os.getenv('TRELLO_KEY')
trello_token = os.getenv('TRELLO_TOKEN')
trello_board_id = os.getenv('TRELLO_BOARD_ID')

app = Flask(__name__)

def extract_trello_lists(response_item):
    return TrelloList(response_item['id'], response_item['name'])

def extract_trello_items(response_item):
    return TrelloCard(response_item['id'], response_item['name'], response_item['idList'])

def make_trello_request(method, endpoint, params):
    app.logger.debug(
    f"""Sending HTTP request to Trello API.
        Method: {method.value}
        URL: {endpoint}
        Parameters: {json.dumps(params)}
    """
    )

    response = requests.request(method.value, endpoint, params=params)
    details = f'{len(response.json())} items found.' if method == "GET" else ''
    app.logger.debug(f'Trello returned {response.status_code}.{details}')

    return response

def get_lists_on_board():
    endpoint = f'{trello_base_url}/boards/{trello_board_id}/lists'
    params = { 'key': trello_key, 'token': trello_token }
    method = HttpMethod.Get
    
    response = make_trello_request(method, endpoint, params)
    return list(map(extract_trello_lists,response.json()))

def get_items_on_board():
    endpoint = f'{trello_base_url}/boards/{trello_board_id}/cards'
    params = { 'key': trello_key, 'token': trello_token }
    method = HttpMethod.Get

    response = make_trello_request(method, endpoint, params)
    return list(map(extract_trello_items,response.json()))

def update_item_list(item_id, list_id):
    endpoint = f'{trello_base_url}/cards/{item_id}'
    params = { 'key': trello_key, 'token': trello_token, 'idList': list_id}
    method = HttpMethod.Put

    make_trello_request(method, endpoint, params)

def create_item(item_name, list_id):
    endpoint = f'{trello_base_url}/cards'
    params = { 'key': trello_key, 'token': trello_token, 'name': item_name, 'idList': list_id}
    method = HttpMethod.Post

    make_trello_request(method, endpoint, params)

def map_trello_items(trello_lists, trello_items):
    items = []
    for trello_item in trello_items:
        for trello_list in trello_lists:
            if (trello_item.listId == trello_list.id):
                items.append(Item(trello_item.id, trello_item.title, trello_list.name))
                break
    return items

def get_id_of_list(name):
    app.logger.debug(f'Getting list with name {name}')
    lists = get_lists_on_board()
    for list in lists:
        if(list.name == name):
            return list.id
    app.logger.debug(f'No list found with name {name}')

@app.route('/')
def index():
    trello_lists = get_lists_on_board()
    trello_items = get_items_on_board()
    
    items = map_trello_items(trello_lists, trello_items)
    return render_template('index.html', items = items)

@app.route('/items/<id>/complete')
def complete_item(id):
    done_list_id = get_id_of_list(ListName.Done.value)
    update_item_list(id, done_list_id)
    return redirect(url_for('index')) 

@app.route('/items/new', methods=['Get'])
def add_item():
    title = request.form['title']
    to_do_list_id = get_id_of_list(ListName.ToDo.value)
    create_item(title, to_do_list_id)
    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run()