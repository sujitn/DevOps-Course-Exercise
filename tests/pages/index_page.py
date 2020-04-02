from selenium.webdriver.common.by import By
from pages.item_element import ItemElement

class IndexPage:

    PAGE_URL = 'http://localhost:5000/'

    # Element selectors
    PAGE_TITLE = (By.TAG_NAME, 'h1')
    TODO_ITEM_CONTAINER = (By.CSS_SELECTOR, 'li.list-group-item')
    NEW_ITEM_NAME_INPUT = (By.ID, 'name-input')
    ADD_ITEM_BUTTON = (By.ID, 'submit-button')

    def __init__(self, browser):
        self.browser = browser

    def visit(self):
        self.browser.get(self.PAGE_URL)

    def is_loaded(self):
        return "To-Do App" in self.browser.find_element(*self.PAGE_TITLE).text

    def todo_list_items(self):
        item_elements = self.browser.find_elements(*self.TODO_ITEM_CONTAINER)
        return [ItemElement(element) for element in item_elements]
    
    def enter_new_item_name(self, name):
        name_input = self.browser.find_element(*self.NEW_ITEM_NAME_INPUT)
        name_input.send_keys(name)
    
    def click_submit_button(self):
        submit_button = self.browser.find_element(*self.ADD_ITEM_BUTTON)
        submit_button.click()
