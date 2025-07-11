"""Web scraper that uses selenium to get data from John Pye Auctions."""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


class Lot:
    """Helper class to store individual lot data."""

    def __init__(self, lot_number: str, description: str,
                 current_bid: str, time_remaining: str) -> None:
        self.lot_number = lot_number
        self.description = description
        self.current_bid = current_bid
        self.time_remaining = time_remaining
        self.retail_price = 0

    def add_retail_price(self, retail_prices: list[WebElement]) -> None:
        """Takes a list of WebElements and extracts the retail price."""
        all_retail_text = [item.text for item in retail_prices]

        retail_text_first_entry = "NO_DATA"
        found = False
        for entry in all_retail_text:
            if entry != "" and not found:
                found = True
                retail_text_first_entry = entry

        if retail_text_first_entry == "NO_DATA":
            self.retail_price = retail_text_first_entry

        retail_text_first_entry_lines = retail_text_first_entry.split("\n")
        price = "NO_DATA"
        found = False
        for line in retail_text_first_entry_lines:
            if line[0] == "£" and not found:
                found = True
                price = line

        self.retail_price = price

    def display_all_lot_info(self) -> None:
        """Prints all lot data in a readable format."""
        print(f"Lot Number: {self.lot_number}")
        print(f"Item Description: {self.description}")
        print(f"Current Bid: {self.current_bid}")
        print(f"Retail Price: {self.retail_price}")


class AuctionContent:
    """Creates a list of Lot objects using data from John Pye Auctions."""

    def __init__(self):
        self.url = "https://www.johnpyeauctions.co.uk/"
        self.search_query = input("Search: ")
        self.service = ""
        self.driver = ""
        self.auction_lots = self.parse_auction_lots(self.scrape_lot_text())

    def multiple_pages(self) -> bool:
        """Checks if there are multiple pages."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pagination")))
            return True
        except TimeoutException:
            return False

    def load_website(self) -> None:
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

    def scrape_lot_text(self) -> str:
        """Searches the website for the search query and returns all of the lots as a string."""
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

        self.load_website()
        self.enter_search_query()

        lot_text = ""
        if False:
            number_of_pages = self.get_number_of_pages()
            for _ in range(number_of_pages):
                lot_text += self.read_page()
                lot_text += "\n"
                self.click_next_page()
        else:
            lot_text += self.read_page()

        self.driver.quit()
        return lot_text

    def get_lot_number(self, lot_line: str) -> str:
        """Takes a line which contains a lot number and returns just the lot number."""
        words = lot_line.split(" ")
        lot_number = f"{words[0]} {words[1]}"
        return lot_number

    def parse_auction_lots(self, lot_text: str) -> list[Lot]:
        """Takes the lot text and returns it as a list of Lot objects."""
        auction_lots = []
        text_lines = lot_text.split("\n")

        for index, line in enumerate(text_lines):
            if "Lot" in line:
                new_lot = Lot(self.get_lot_number(line),
                              text_lines[index+1], text_lines[index+4], text_lines[index+5])
                auction_lots.append(new_lot)

        return auction_lots


class PriceCheck:
    """Searches for retail prices of Lot objects using bing."""

    def __init__(self, auction_lots: list[Lot]) -> None:
        self.auction_lots = auction_lots
        self.item_descriptions = [lot.description for lot in auction_lots]
        self.url = "https://www.bing.com/"
        self.service = ""
        self.driver = ""

    def is_shopping_tab(self) -> bool:
        """Checks if there is a shopping tab."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "b-scopeListItem-shop")))
            return True
        except TimeoutException:
            return False

    def get_retail_prices(self) -> None:
        """Searches lot descriptions on bing and updates lot retail prices."""
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get(self.url)

        time.sleep(5)
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "bnp_btn_accept"))
        ).click()

        for i in range(len(self.item_descriptions)):
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_bar = self.driver.find_element(By.NAME, "q")
            search_bar.send_keys(self.item_descriptions[i])

            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "search_icon"))
            ).click()

            if self.is_shopping_tab():
                original_window = self.driver.current_window_handle

                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "b-scopeListItem-shop"))
                ).click()

                WebDriverWait(self.driver, 5).until(
                    EC.number_of_windows_to_be(2))

                for window_handle in self.driver.window_handles:
                    if window_handle != original_window:
                        self.driver.switch_to.window(window_handle)
                        break

                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "slide")))

                items = self.driver.find_elements(By.CLASS_NAME, "slide")
                self.auction_lots[i].add_retail_price(items)

                self.driver.close()
                self.driver.switch_to.window(original_window)

            else:
                self.auction_lots[i].retail_price = "NO_DATA"

            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "b_logoArea"))
            ).click()

            time.sleep(2)

        self.driver.quit()


if __name__ == "__main__":
    auction = AuctionContent()
    price_check = PriceCheck(auction.auction_lots)
    price_check.get_retail_prices()
    for lot in price_check.auction_lots:
        lot.display_all_lot_info()
        print("\n")
