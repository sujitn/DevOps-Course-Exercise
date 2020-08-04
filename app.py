from flask import Flask, render_template, request, redirect, url_for
import session_items as session
from item import TrelloItem
from trello import TrelloClient
from viewModel import ViewModel
import os

app = Flask(__name__)
app.config.from_object('flask_config.Config')

client = TrelloClient(
    api_key=os.environ.get('TRELLO_API_KEY'),
    token=os.environ.get('TRELLO_TOKEN')
)


board = client.get_board(os.environ.get('TRELLO_BOARD_ID'))

@app.route('/')
def index():
    
    items = []

    board_lists = board.list_lists()
    for list_item in board_lists:
        for card in list_item.list_cards():
            items.append(TrelloItem(card.id, list_item.name,card.name, card.dateLastActivity))

    item_view_model = ViewModel(items)
    return render_template('index.html', view_model=item_view_model)

@app.route('/items/new', methods=['POST'])
def add_item():
    title = request.form['title']
    
    board_lists = board.list_lists()
    todo_list = next((x for x in board_lists if x.name == "ToDo"), None)

    todo_list.add_card(title);  
    return redirect(url_for('index')) 

@app.route('/items/<id>/complete')
def complete_item(id):

    board_lists = board.list_lists()
    todo_list = next((x for x in board_lists if x.name == "ToDo"), None)
    done_list = next((x for x in board_lists if x.name == "Done"), None)
    
    cards = todo_list.list_cards()
    card = next((x for x in cards if x.id == id), None)   
    card.change_list(done_list.id)  
    return redirect(url_for('index')) 
    
@app.route('/items/<id>/uncomplete')
def uncomplete_item(id):
    board_lists = board.list_lists()
    todo_list = next((x for x in board_lists if x.name == "ToDo"), None)
    done_list = next((x for x in board_lists if x.name == "Done"), None)
    
    cards = done_list.list_cards()
    card = next((x for x in cards if x.id == id), None)   
    card.change_list(todo_list.id)  
    return redirect(url_for('index')) 


if __name__ == '__main__':
    app.run()
