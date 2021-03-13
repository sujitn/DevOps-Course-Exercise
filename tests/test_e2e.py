import os
import time
from threading import Thread
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import find_dotenv, load_dotenv
import requests

import app

TRELLO_BASE_URL = 'https://api.trello.com/1'
TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')

def create_trello_board():
    response = requests.post(
        url=f'{TRELLO_BASE_URL}/boards',
        params={
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
            'name': 'Selenium Test Board'
        }
    )
    return response.json()['id']


def delete_trello_board(board_id):
    requests.delete(
        url=f'{TRELLO_BASE_URL}/boards/{board_id}',
        params={
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
        }
    )
    
def create_list(list_name):
    response = requests.post(
            url=f'{TRELLO_BASE_URL}/lists',
            params={
                'key': TRELLO_API_KEY,
                'token': TRELLO_TOKEN,
                'name': list_name,
                'idBoard': os.getenv("TRELLO_BOARD_ID"),
            }
        )
    return response.json()['id']

    
@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv()
    load_dotenv(file_path, override=True)
    # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    
    create_list('ToDo')
    create_list('Done')

    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)


@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver


def test_task_journey(driver, test_app):
    driver.implicitly_wait(3)
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

    add_new_task(driver)
    #start_task(driver)
    #complete_task(driver)
    #mark_test_as_incomplete(driver)


def add_new_task(driver):
    new_task_input = driver.find_element_by_name("title")
    new_task_input.send_keys('Test Task')
    driver.find_element_by_xpath("//button[contains(text(), 'Add Item')]").click()

    assert find_task_in_section('todo-section', driver) is not None


def start_task(driver):
    task = find_task_in_section('todo-section', driver)
    task.find_element_by_link_text('Start').click()

    assert find_task_in_section('doing-section', driver) is not None


def complete_task(driver):
    task = find_task_in_section('doing-section', driver)
    task.find_element_by_link_text('Complete').click()

    assert find_task_in_section('done-section', driver) is not None


def mark_test_as_incomplete(driver):
    task = find_task_in_section('done-section', driver)
    task.find_element_by_link_text('Mark as Incomplete').click()

    assert find_task_in_section('todo-section', driver) is not None


def find_task_in_section(section_name, driver):
    section = driver.find_element_by_xpath(f"//*[@data-test-id='{section_name}']")
    tasks = section.find_elements_by_xpath("//*[@data-test-class='task']")
    return next(task for task in tasks if task.find_element_by_xpath("//*[contains(text(), 'Test Task')]") is not None)