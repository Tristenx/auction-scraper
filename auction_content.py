from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class AuctionContent:
    def __init__(self):
        self.text = []
        self.lot_numbers = []
        self.item_descriptions = []
        self.current_bids = []
        self.time_remaining = []

    def read_content(self):
        with open(file="search_results.txt", mode="r") as file:
            self.text = file.read()

        lines = self.text.split("\n")
        for i in range(len(lines)):
            words = lines[i].split(" ")
            if words[0] == "Lot":
                self.lot_numbers.append(words[1])
                self.item_descriptions.append(lines[i+1])
                self.current_bids.append(lines[i+4])
                self.time_remaining.append(lines[i+5])

    def read_page(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "row")))

        item = self.driver.find_element(
            By.XPATH, "/html/body/main/div/div[2]/div[2]/div[3]/div")

        with open(file="search_results.txt", mode="a") as file:
            file.write(item.text)

    def multiple_pages(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pagination")))
            return True
        except:
            return False

    def scrape_data(self):
        item = input("SEARCH: ")

        with open(file="search_results.txt", mode="w") as file:
            file.write("")

        # ---------------------------- LOAD WEBSITE ------------------------------- #
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

        self.driver.get("https://www.johnpyeauctions.co.uk/")

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "cc-nb-okagree")))

        accept_button = self.driver.find_element(
            By.CLASS_NAME, "cc-nb-okagree")
        accept_button.click()

        # ---------------------------- SEARCH FOR ITEM ------------------------------- #
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "FullTextQuery1")))

        input_element = self.driver.find_element(By.ID, "FullTextQuery1")
        input_element.clear()
        input_element.send_keys(item + Keys.ENTER)

        # ---------------------------- READ PAGES ------------------------------- #
        if self.multiple_pages():
            page_navigator = self.driver.find_element(
                By.CLASS_NAME, "pagination")
            num_pages = int(page_navigator.text[-3])

            for i in range(num_pages):
                self.read_page()
                next_page = self.driver.find_element(
                    By.XPATH, '//ul[@class="pagination"]//a[text()="»"]')
                next_page.click()
        else:
            self.read_page()

        self.driver.quit()
