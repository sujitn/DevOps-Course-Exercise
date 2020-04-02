import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options = options, executable_path = r'bin/chromedriver')
    driver.implicitly_wait(10)
    yield driver
    driver.close()
