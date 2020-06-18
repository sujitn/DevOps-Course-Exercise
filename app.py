import os
from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import requests
import TrelloList from entity.list

import sys
import json

trello_base_url = os.getenv('TRELLO_API_BASE_URL')
trello_key = os.getenv('TRELLO_KEY')
trello_token = os.getenv('TRELLO_TOKEN')
trello_board_id = os.getenv('TRELLO_BOARD_ID')

app = Flask(__name__)
app.config.from_object('flask_config.Config')

def extract_trello_lists(response_item):
    return  {
        'id': response_item['id'],
        'name': response_item['name'],
    }

def get_lists_on_board():
    endpoint = trello_base_url + '/1/boards/' + trello_board_id + '/lists'
    params = { 'key': trello_key, 'token': trello_token }
    app.logger.debug('Fetching lists from Trello board.\n\tMethod: Get\n\tURL: ' + endpoint + '\n\tParameters: ' + json.dumps(params))
    
    response = requests.request(
        "GET",
        endpoint,
        params=params
    )
    app.logger.debug('Trello returned ' + str(response.status_code) + '. ' + str(len(response.json())) + ' items found.')
    return list(map(extract_trello_lists,response.json()))

def get_items_on_board():
    endpoint = trello_base_url + '/1/boards/' + trello_board_id + '/cards'
    params = { 'key': trello_key, 'token': trello_token }
    app.logger.debug('Fetching items from Trello board.\n\tMethod: Get\n\tURL: ' + endpoint + '\n\tParameters: ' + json.dumps(params))
    
    response = requests.request(
        "GET",
        endpoint,
        params=params
    )
    app.logger.debug('Trello returned ' + str(response.status_code) + '. ' + str(len(response.json())) + ' items found.')
    return list(map(extract_trello_items,response.json()))

def update_item_list(item_id, list_id):
    endpoint = trello_base_url + '/1/cards/' + item_id
    params = {
        'key': trello_key,
        'token': trello_token,
        'idList': list_id
        }
    app.logger.debug('Updating item on Trello board.\n\tMethod: Put\n\tURL: ' + endpoint + '\n\tParameters: ' + json.dumps(params))
    
    response = requests.request(
        "PUT",
        endpoint,
        params=params
    )
    app.logger.debug('Trello returned ' + str(response.status_code))

def extract_trello_items(response_item):
    return  {
        'id': response_item['id'],
        'title': response_item['name'],
        'listId': response_item['idList'],
    }

def map_trello_items(trello_lists, trello_items):
    items = []
    for trello_item in trello_items:
        for trello_list in trello_lists:
            if (trello_item['listId'] == trello_list['id']):
                items.append({
                    'id' : trello_item['id'],
                    'title': trello_item['title'],
                    'status': trello_list['name']
                    })
                break
    return items

def get_id_of_list(name):
    app.logger.debug('Getting list with name ' + name)
    lists = get_lists_on_board()
    for list in lists:
        if(list['name'] == name):
            return list['id']
    app.logger.debug('No list found with name ' + name)

@app.route('/')
def index():
    trello_lists = get_lists_on_board()
    trello_items = get_items_on_board()
    
    items = map_trello_items(trello_lists, trello_items)
    return render_template('index.html', items = items)

@app.route('/items/<id>/complete')
def complete_item(id):
    done_list_id = get_id_of_list('Done')
    update_item_list(id, done_list_id)
    return redirect(url_for('index')) 


if __name__ == '__main__':
    app.run()