from trello_requests.boards import create_board, delete_board
from app import create_app
import os
from threading import Thread
from selenium import webdriver
import pytest
from dotenv import find_dotenv, load_dotenv

import logging
log = logging.getLogger('app')


@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv()
    load_dotenv(file_path, override=True)

    # Create the new board & update the board id environment variable
    board_id = create_board('test-name')
    os.environ['TRELLO_BOARD_ID'] = board_id

    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    delete_board(board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
