from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class WebNavigator:
    def __init__(self):
        self.timeout = None
        self.web_driver = None

    def launch_browser(self, website_url):
        self.web_driver = webdriver.Chrome()
        self.open_website(website_url)
        return self.web_driver

    def fetch_wait(self, timeout=10):
        self.timeout = timeout
        return WebDriverWait(self.web_driver, self.timeout)

    def open_website(self, website_url):
        self.web_driver.get(website_url)

    def terminate_browser(self):
        if self.web_driver:
            self.web_driver.quit()
