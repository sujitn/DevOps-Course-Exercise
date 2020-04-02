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
