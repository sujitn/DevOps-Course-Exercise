from selenium.webdriver.common.by import By

class ItemElement:

    # Element selectors
    ITEM_NAME = (By.TAG_NAME, 'h5')
    ITEM_STATUS = (By.CLASS_NAME, 'badge')
    ACTION_BUTTON = (By.CLASS_NAME, 'btn')
    START_BUTTON = (By.CLASS_NAME, 'btn-success')
    COMPLETE_BUTTON = (By.CLASS_NAME, 'btn-primary')
    RESET_BUTTON = (By.CLASS_NAME, 'btn-secondary')

    def __init__(self, element):
        self.element = element

    @property
    def name(self):
        return self.element.find_element(*self.ITEM_NAME).text

    @property
    def status(self):
        return self.element.find_element(*self.ITEM_STATUS).text

    def has_start_button(self):
        return len(self.element.find_elements(*self.START_BUTTON)) > 0

    def has_complete_button(self):
        return len(self.element.find_elements(*self.COMPLETE_BUTTON)) > 0

    def has_complete_button(self):
        return len(self.element.find_elements(*self.RESET_BUTTON)) > 0

    def start(self):
        button = self.element.find_element(*self.START_BUTTON)
        button.click()

    def complete(self):
        button = self.element.find_element(*self.COMPLETE_BUTTON)
        button.click()
