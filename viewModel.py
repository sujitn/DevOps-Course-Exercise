from item import Item
from datetime import date


class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return [item for item in self._items if item.status == 'ToDo']

    @property
    def doing_items(self):
        return [item for item in self._items if item.status == 'Doing']

    @property
    def done_items(self):
        return [item for item in self._items if item.status == 'Done']

    @property
    def show_all_done_items(self):
        return len(self.done_items) <= 3

    @property
    def recent_done_items(self):
        return [item for item in self.done_items if item.last_modified.date() == date.today()]

    @property
    def older_done_items(self):
        return [item for item in self.done_items if not item.last_modified.date() == date.today()]
