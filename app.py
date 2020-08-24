from flask import Flask, render_template, request, redirect, url_for
import session_items as session
from item import TrelloItem
from trello import TrelloClient
from viewModel import ViewModel
import os

def get_trello_board(api_key, token, board_id):
        client = TrelloClient(
            api_key=api_key,
            token=token
        )
        
        return client.get_board(board_id)
        
    
def get_items(api_key, token, board_id):
    items = []
    board = get_trello_board(api_key, token, board_id)
    board_lists = board.list_lists()
    for list_item in board_lists:
        for card in list_item.list_cards():
            items.append(TrelloItem(card.id, list_item.name,card.name, card.dateLastActivity))
            
    return items

def create_app():
    app = Flask(__name__)
    app.config.from_object('flask_config.Config')
    
    api_key=app.config['TRELLO_API_KEY']
    token=app.config['TRELLO_TOKEN']
    board_id = app.config['TRELLO_BOARD_ID']

    @app.route('/')
    def index():
        items = get_items(api_key, token, board_id)
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/items/new', methods=['POST'])
    def add_item():
        title = request.form['title']
        board = get_trello_board(api_key, token, board_id)
        board_lists = board.list_lists()
        todo_list = next((x for x in board_lists if x.name == "ToDo"), None)

        todo_list.add_card(title);  
        return redirect(url_for('index')) 

    @app.route('/items/<id>/complete')
    def complete_item(id):
        board = get_trello_board(api_key, token, board_id)
        board_lists = board.list_lists()
        todo_list = next((x for x in board_lists if x.name == "ToDo"), None)
        done_list = next((x for x in board_lists if x.name == "Done"), None)
        
        cards = todo_list.list_cards()
        card = next((x for x in cards if x.id == id), None)   
        card.change_list(done_list.id)  
        return redirect(url_for('index')) 
        
    @app.route('/items/<id>/uncomplete')
    def uncomplete_item(id):
        board = get_trello_board(api_key, token, board_id)
        board_lists = board.list_lists()
        todo_list = next((x for x in board_lists if x.name == "ToDo"), None)
        done_list = next((x for x in board_lists if x.name == "Done"), None)
        
        cards = done_list.list_cards()
        card = next((x for x in cards if x.id == id), None)   
        card.change_list(todo_list.id)  
        return redirect(url_for('index')) 
        
    return app
   


if __name__ == '__main__':
    create_app().run()
