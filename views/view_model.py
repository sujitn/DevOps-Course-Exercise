from entity.list_name import ListName

from helpers.index import filter_items_by_list

class ViewModel:
  def __init__(self, items):
    self._items = items

  @property
  def all_items(self):
    return self._items

  @property
  def to_do_items(self):
    return filter_items_by_list(self._items, ListName.ToDo.value)

  @property
  def doing_items(self):
    return filter_items_by_list(self._items, ListName.Doing.value)

  @property
  def done_items(self):
    return filter_items_by_list(self._items, ListName.Done.value)