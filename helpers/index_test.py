import pytest

from entity.list_name import ListName
from entity.item import Item

from helpers.index import filter_items_by_list


@pytest.fixture
def to_do_item():
    item = Item('to-do-id', 'to-do-title', ListName.ToDo.value)
    return item


@pytest.fixture
def doing_item():
    item = Item('doing-id', 'doing-title', ListName.Doing.value)
    return item


@pytest.fixture
def done_item():
    item = Item('done-id', 'done-title', ListName.Done.value)
    return item


def test_filter_items_picks_out_to_do_items(to_do_item, doing_item, done_item):
    unfiltered_list = [to_do_item, doing_item, done_item]

    filtered_items = filter_items_by_list(unfiltered_list, ListName.ToDo.value)

    assert len(filtered_items) == 1
    assert filtered_items[0].title == to_do_item.title


def test_filter_items_handles_multiple_to_do_items(to_do_item, doing_item, done_item):
    unfiltered_list = [to_do_item, doing_item, to_do_item, done_item]

    filtered_items = filter_items_by_list(unfiltered_list, ListName.ToDo.value)

    assert len(filtered_items) == 2
    assert filtered_items[0].title == to_do_item.title
    assert filtered_items[1].title == to_do_item.title


def test_filter_items_handles_no_to_do_items(to_do_item, doing_item, done_item):
    unfiltered_list = [doing_item, done_item]

    filtered_items = filter_items_by_list(unfiltered_list, ListName.ToDo.value)

    assert len(filtered_items) == 0


def test_filter_items_handles_empty_items(to_do_item, doing_item, done_item):
    unfiltered_list = []

    filtered_items = filter_items_by_list(unfiltered_list, ListName.ToDo.value)

    assert len(filtered_items) == 0
