from flask import Flask, render_template, request, redirect, url_for
import session_items as session
from item import Item
from trello import TrelloClient
from viewModel import ViewModel
import os
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def get_trello_board(api_key, token, board_id):
    client = TrelloClient(
        api_key=api_key,
        token=token
    )

    return client.get_board(board_id)


def get_items(collection):
    items = []

    for item in collection.find():
        items.append(
            Item(
                item['_id'],
                item['status'],
                item['title'],
                item['last_modified']
            )
        )

    return items


def add_new_item(collection, title):
    collection.insert_one(
        {
            "title": title,
            "status": 'ToDo',
            "last_modified": datetime.now()
        }
    )


def mark_item_as_complete(collection, id):
    collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": 'Done',
                "last_modified": datetime.now()
            }
        }
    )


def mark_item_as_uncomplete(collection, id):
    collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": 'ToDo',
                "last_modified": datetime.now()
            }
        }
    )


def get_db_collection():
    dbClientUri = f"mongodb+srv://{os.getenv('MONGO_DB_USER_NAME')}:{os.getenv('MONGO_DB_PASSWORD')}@cluster0.59kpk.mongodb.net/?retryWrites=true&w=majority"
    databaseName = os.getenv('MONGO_DB_DATABASE_NAME')
    collectionName = 'collection'

    dbClient = pymongo.MongoClient(dbClientUri)
    db = dbClient[databaseName]
    return db[collectionName]


def create_app():
    app = Flask(__name__)
    app.config.from_object('flask_config.Config')

    collection = get_db_collection()

    @app.route('/')
    def index():
        items = get_items(collection)
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/items/new', methods=['POST'])
    def add_item():
        title = request.form['title']
        add_new_item(collection, title)
        return redirect(url_for('index'))

    @app.route('/items/<id>/complete')
    def complete_item(id):
        mark_item_as_complete(collection, id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/uncomplete')
    def uncomplete_item(id):
        mark_item_as_uncomplete(collection, id)
        return redirect(url_for('index'))

    return app


if __name__ == '__main__':
    create_app().run()
