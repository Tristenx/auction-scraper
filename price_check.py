import time
from auction_content import AuctionContent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class PriceCheck:
    def __init__(self, auction_lots: list[dict]):
        self.item_descriptions = [lot["description"]
                                  for lot in auction_lots]
        self.current_bids = [lot["current_bid"]
                             for lot in auction_lots]
        self.url = "https://www.bing.com/"
        self.service = ""
        self.driver = ""
        self.prices = []

    def get_retail_prices(self):
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

            try:
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
                print(items[7].text)
                # for i in range(len(items)):
                #     with open(file="price_data.txt", mode="a") as file:
                #         if items[i].text != "":
                #             file.write(f"{i} {items[i].text}")
                #             file.write("\n\n")

                # with open(file="price_data.txt", mode="a") as file:
                #     file.write("END\n\n")

                self.driver.close()
                self.driver.switch_to.window(original_window)

            except:
                print("NO_DATA")
                # with open(file="price_data.txt", mode="a") as file:
                #     file.write("NO DATA\n\n")
                #     file.write("END\n\n")

            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "b_logoArea"))
            ).click()

            time.sleep(2)

        self.driver.quit()


auction_content = AuctionContent()
price_check = PriceCheck(auction_content.auction_lots)
price_check.get_retail_prices()
