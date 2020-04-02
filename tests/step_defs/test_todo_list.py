import pytest
from pytest_bdd import scenarios, given, when, then
from pages.index_page import IndexPage

# Scenarios

scenarios('../features/todo_list.feature')

# Given Steps

@given('there are existing items')
def setup_existing_items():
    pass

# When Steps

@when('I am on the index page')
def visit_index_page(browser):
    page = IndexPage(browser)
    page.visit()

# Then Steps

@then('I can see a list of items')
def items_are_dispayed(browser):
    page = IndexPage(browser)
    items = page.todo_list_items()
    assert len(items) > 0

@then('done items are listed after todo items')
def done_items_listed_after_todo_items(browser):
    page = IndexPage(browser)
    items = page.todo_list_items()
    todo_item_indices = [index for index, item in enumerate(items) if item.status == 'To Do']
    done_item_indices = [index for index, item in enumerate(items) if item.status == 'Done']
    assert todo_item_indices[-1] < done_item_indices[0]

@then('all todo items have a start button')
def all_todo_items_have_start_buttons(browser):
    page = IndexPage(browser)
    items = page.todo_list_items()
    todo_items = [item for item in items if item.status == 'To Do']
    assert all(item.has_start_button() for item in todo_items)
