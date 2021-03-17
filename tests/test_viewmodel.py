from datetime import date, datetime, timedelta

from item import Item
from viewModel import ViewModel


def test_items_by_status():
    items = [
        Item(1, 'ToDo', 'Task 1', date.today()),
        Item(2, 'Done', 'Task 2', date.today()),
        Item(3, 'ToDo', 'Task 3', date.today()),
        Item(4, 'Doing', 'Task 4', date.today())
    ]

    view_model = ViewModel(items)
    print(view_model.todo_items)
    assert view_model.todo_items == [
        item for item in items if item.status == 'ToDo']
    assert view_model.doing_items == [
        item for item in items if item.status == 'Doing']
    assert view_model.done_items == [
        item for item in items if item.status == 'Done']


def test_show_done_items_if_less_than_3():
    items = [
        Item(1, 'Done', 'Task 1', date.today()),
        Item(2, 'Done', 'Task 2', date.today()),
        Item(3, 'Doing', 'Task 3', date.today()),
        Item(4, 'Done', 'Task 4', date.today()),
    ]

    view_model = ViewModel(items)

    assert view_model.show_all_done_items is True


def test_hide_done_items_if_greater_than_3():
    items = [
        Item(1, 'Done', 'Task 1', date.today()),
        Item(2, 'Done', 'Task 2', date.today()),
        Item(3, 'Done', 'Task 3', date.today()),
        Item(4, 'Done', 'Task 4', date.today()),
    ]

    view_model = ViewModel(items)

    assert view_model.show_all_done_items is False


def test_recent_items_contain_today_done_items():
    items = [
        Item(1, 'Done', 'Task 1', datetime.now()),
        Item(2, 'Done', 'Task 2', datetime.now() - timedelta(days=1)),
        Item(3, 'Doing', 'Task 3', datetime.now() - timedelta(hours=1)),
    ]

    view_model = ViewModel(items)
    assert view_model.recent_done_items == [
        item for item in items if item.id == 1]


def test_older_items_contain_today_done_items():
    items = [
        Item(1, 'Done', 'Task 1', datetime.now()),
        Item(2, 'Done', 'Task 2', datetime.now() - timedelta(days=1)),
        Item(3, 'Doing', 'Task 3', datetime.now() - timedelta(hours=1)),
        Item(4, 'Done', 'Task 2', datetime.now() - timedelta(days=2)),
    ]

    view_model = ViewModel(items)
    assert view_model.older_done_items == [
        item for item in items if item.last_modified.date() < date.today()]
