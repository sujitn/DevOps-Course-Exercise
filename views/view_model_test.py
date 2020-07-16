import pytest

from entity.list_name import ListName
from entity.item import Item
from views.view_model import ViewModel

@pytest.fixture
def viewModel():
  to_do_item = Item('to-do-id', 'to-do-title', ListName.ToDo.value)
  doing_item = Item('doing-id', 'doing-title', ListName.Doing.value)
  done_item = Item('done-id', 'done-title', ListName.Done.value)
  return ViewModel([to_do_item, doing_item, done_item])

def test_toDoItems_returns_to_do_items(viewModel):
    assert len(viewModel.to_do_items) == 1
    assert viewModel.to_do_items[0].title == 'to-do-title'

def test_toDoItems_returns_doing_items(viewModel):
    assert len(viewModel.doing_items) == 1
    assert viewModel.doing_items[0].title == 'doing-title'

def test_toDoItems_returns_done_items(viewModel):
    assert len(viewModel.done_items) == 1
    assert viewModel.done_items[0].title == 'done-title'