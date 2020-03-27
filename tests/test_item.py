from todo_item import Item

def test_item_uses_specified_id():
    # Arrange
    id = '1'
    # Act
    item = Item(id, 'Item 1')
    # Assert
    assert item.id == id

def test_item_uses_specified_name():
    # Arrange
    name = 'Item 1'
    # Act
    item = Item('1', name)
    # Assert
    assert item.name == name

def test_item_is_created_with_todo_status():
    # Arrange
    item = Item('1', 'Item 1')
    # Assert
    assert item.status == 'To Do'

def test_item_start_sets_status_to_doing():
    # Arrange
    item = Item('1', 'Item 1')
    # Act
    item.start()
    # Assert
    assert item.status == 'Doing'

def test_item_complete_sets_status_to_done():
    # Arrange
    item = Item('1', 'Item 1')
    # Act
    item.complete()
    # Assert
    assert item.status == 'Done'

def test_item_reset_sets_status_to_todo():
    # Arrange
    item = Item('1', 'Item 1', status = 'Done')
    # Act
    item.reset()
    # Assert
    assert item.status == 'To Do'

def test_fromTrelloCard_creates_item_with_card_properties():
    # Arrange
    card_id = '1'; card_name = 'Card 1'; list_name = 'List 1'
    trello_card = { 'id': card_id, 'name': card_name }
    trello_list = { 'name': list_name }
    # Act
    item = Item.fromTrelloCard(trello_card, trello_list)
    # Assert
    assert item.id == card_id
    assert item.name == card_name
    assert item.status == list_name
