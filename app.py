from flask import Flask, render_template, request, redirect, url_for
import session_items as session
from item import Item
from viewModel import ViewModel
import os
import pymongo
import random
import string
from datetime import datetime
from bson.objectid import ObjectId
import requests
from user import User
from user_role import UserRole
from flask_login import LoginManager, login_required, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient
from writer_role_decorator import require_writer

date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"


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
    login_disabled = os.getenv('LOGIN_DISABLED').upper() == 'TRUE'
    app.config['LOGIN_DISABLED'] = login_disabled

    collection = get_db_collection()

    login_manager = LoginManager()

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    state = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
    oauth_client = WebApplicationClient(client_id)

    @login_manager.unauthorized_handler
    def unauthenticated():
        request_uri = oauth_client.prepare_request_uri(
            "https://github.com/login/oauth/authorize",
            state=state
        )
        return redirect(request_uri)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    @app.route("/login/callback", methods=["GET"])
    def callback():
        token_request_url, token_request_headers, token_request_body = oauth_client.prepare_token_request(
            token_url="https://github.com/login/oauth/access_token",
            authorization_response=request.url,
            state=state,
            client_secret=client_secret
        )
        token_response = requests.post(
            token_request_url,
            headers=token_request_headers,
            data=token_request_body
        )
        oauth_client.parse_request_body_response(
            token_response.content.decode(),
            state=state
        )

        user_info_request_url, user_info_request_headers, user_info_request_body = oauth_client.add_token(
            uri='https://api.github.com/user',
        )
        user_info_response = requests.get(
            user_info_request_url,
            data=user_info_request_body,
            headers=user_info_request_headers
        )

        github_username = user_info_response.json()['login']
        user = User(github_username)
        login_success = login_user(user)

        if login_success:
            return redirect(url_for('index'))
        else:
            return "Unauthorised", 403

    @app.route('/')
    @login_required
    def index():
        user: User = current_user
        readonly = (not login_disabled) and user.get_role() == UserRole.Reader
        items = get_items(collection)
        item_view_model = ViewModel(items, readonly)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/items/new', methods=['POST'])
    @require_writer
    @login_required
    def add_item():
        title = request.form['title']
        add_new_item(collection, title)
        return redirect(url_for('index'))

    @app.route('/items/<id>/complete')
    @require_writer
    @login_required
    def complete_item(id):
        mark_item_as_complete(collection, id)
        return redirect(url_for('index'))

    @app.route('/items/<id>/uncomplete')
    @require_writer
    @login_required
    def uncomplete_item(id):
        mark_item_as_uncomplete(collection, id)
        return redirect(url_for('index'))

    return app


if __name__ == '__main__':
    create_app().run()
