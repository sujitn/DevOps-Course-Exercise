import os
import time
from threading import Thread
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import find_dotenv, load_dotenv
import requests
import random
import string
import pymongo
import app


def get_db_collection(database):
    dbClientUri = f"mongodb+srv://{os.getenv('MONGO_DB_USER_NAME')}:{os.getenv('MONGO_DB_PASSWORD')}@cluster0.59kpk.mongodb.net/?retryWrites=true&w=majority"
    databaseName = database
    collectionName = 'collection'

    dbClient = pymongo.MongoClient(dbClientUri)
    db = dbClient[databaseName]
    return db[collectionName]


@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv()
    load_dotenv(file_path, override=True)

    db_name = 'test-table-' + \
        ''.join(random.choice(string.ascii_uppercase + string.digits)
                for _ in range(10))
    collection = get_db_collection(db_name)

    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    collection.drop()


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
    # start_task(driver)
    # complete_task(driver)
    # mark_test_as_incomplete(driver)


def add_new_task(driver):
    new_task_input = driver.find_element_by_name("title")
    new_task_input.send_keys('Test Task')
    driver.find_element_by_xpath(
        "//button[contains(text(), 'Add Item')]").click()

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
    section = driver.find_element_by_xpath(
        f"//*[@data-test-id='{section_name}']")
    tasks = section.find_elements_by_xpath("//*[@data-test-class='task']")
    return next(task for task in tasks if task.find_element_by_xpath("//*[contains(text(), 'Test Task')]") is not None)
