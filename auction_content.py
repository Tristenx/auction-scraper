"""Contains the auction content class which uses selenium to scrape data from the auction site."""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class AuctionContent:
    """Stores lot data as a list of dictionaries and contains functions to scrape this data."""

    def __init__(self):
        self.url = "https://www.johnpyeauctions.co.uk/"
        self.search_query = input("Search: ")
        self.service = ""
        self.driver = ""
        self.lots = []

    def multiple_pages(self) -> bool:
        """Checks if there are multiple pages."""
        if WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pagination"))):
            return True
        return False

    def load_website(self):
        """Loads the website and accepts cookies."""
        self.driver.get(self.url)

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "cc-nb-okagree")))

        accept_button = self.driver.find_element(
            By.CLASS_NAME, "cc-nb-okagree")
        accept_button.click()

    def enter_search_query(self):
        """Types search query in the search bar and hits enter."""
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "FullTextQuery1")))

        search_bar = self.driver.find_element(By.ID, "FullTextQuery1")
        search_bar.clear()
        search_bar.send_keys(self.search_query + Keys.ENTER)

    def read_page(self) -> str:
        """Searches for the element which contains the lots then returns its text as a string."""
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "row")))

        target_element = self.driver.find_element(
            By.XPATH, "/html/body/main/div/div[2]/div[2]/div[3]/div")
        return target_element.text

    def click_next_page(self):
        """Clicks the next page button."""
        next_page = self.driver.find_element(
            By.XPATH, '//ul[@class="pagination"]//a[text()="»"]')
        next_page.click()

    def get_number_of_pages(self) -> int:
        """Returns the number of pages."""
        page_navigator = self.driver.find_element(
            By.CLASS_NAME, "pagination")
        number_of_pages = int(page_navigator.text[-3])
        return number_of_pages

    def get_lots(self) -> str:
        """Searches the website for the search query and returns all of the lots as a string."""
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

        self.load_website()
        self.enter_search_query()

        lots = ""
        if self.multiple_pages():
            number_of_pages = self.get_number_of_pages()
            for _ in range(number_of_pages):
                lots += self.read_page()
                lots += "\n"
                self.click_next_page()
        else:
            lots += self.read_page()

        self.driver.quit()
        return lots


auction_content = AuctionContent()
print(auction_content.get_lots())
