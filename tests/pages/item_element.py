from selenium.webdriver.common.by import By

class ItemElement:

    # Element selectors
    ITEM_NAME = (By.TAG_NAME, 'h5')
    ITEM_STATUS = (By.CLASS_NAME, 'badge')
    ACTION_BUTTON = (By.CLASS_NAME, 'btn')

    def __init__(self, element):
        self.element = element

    @property
    def name(self):
        return self.element.find_element(*self.ITEM_NAME).text

    @property
    def status(self):
        return self.element.find_element(*self.ITEM_STATUS).text
