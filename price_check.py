from auction_content import AuctionContent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PriceCheck:
    def __init__(self, content: AuctionContent):
        self.items = content.item_descriptions
        self.bids = content.current_bids
        self.prices = []

    def get_price_data(self):
        with open(file="price_data.txt", mode="w") as file:
            file.write("")

        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.bing.com/")

        try:
            time.sleep(5)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "bnp_btn_accept"))
            ).click()
        except:
            pass

        for i in range(len(self.items)):
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(self.items[i])

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "search_icon"))
            ).click()

            original_window = driver.current_window_handle

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "b-scopeListItem-shop"))
            ).click()

            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "slide")))

            items = driver.find_elements(By.CLASS_NAME, "slide")
            for i in range(len(items)):
                with open(file="price_data.txt", mode="a") as file:
                    if items[i].text != "":
                        file.write(f"{i} {items[i].text}")
                        file.write("\n\n")

            with open(file="price_data.txt", mode="a") as file:
                file.write("END\n\n")

            driver.close()
            driver.switch_to.window(original_window)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "b_logoArea"))
            ).click()

            time.sleep(2)

        driver.quit()

    def read_price_data(self):
        with open(file="price_data.txt", mode="r") as file:
            content = file.read()

        content = content.split("\n\n")
        item_prices = []
        new_item = []
        for entry in content:
            if entry == "END":
                item_prices.append(new_item)
                new_item = []
            else:
                entry = entry.split("\n")
                if len(entry) != 1:
                    new_item.append(entry[1])

        return item_prices

    def calculate_prices(self):
        pass
