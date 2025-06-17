from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_page():
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "row")))

    items = driver.find_elements(
        By.CLASS_NAME, "row")

    with open(file="search_results.txt", mode="a") as file:
        for item in items:
            file.write(f"{item.text}\n")


def multiple_pages():
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pagination")))
        return True
    except:
        return False


# ---------------------------- RESET SEARCH RESULTS ------------------------------- #
item = input("SEARCH: ")

with open(file="search_results.txt", mode="w") as file:
    file.write("")

# ---------------------------- LOAD WEBSITE ------------------------------- #
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.johnpyeauctions.co.uk/")

WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable(
        (By.CLASS_NAME, "cc-nb-okagree")))

accept_button = driver.find_element(By.CLASS_NAME, "cc-nb-okagree")
accept_button.click()

# ---------------------------- SEARCH FOR ITEM ------------------------------- #
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "FullTextQuery1")))

input_element = driver.find_element(By.ID, "FullTextQuery1")
input_element.clear()
input_element.send_keys(item + Keys.ENTER)

# ---------------------------- READ PAGES ------------------------------- #
if multiple_pages():
    page_navigator = driver.find_element(By.CLASS_NAME, "pagination")
    num_pages = int(page_navigator.text[-3])

    for i in range(num_pages):
        read_page()
        next_page = driver.find_element(
            By.XPATH, '//ul[@class="pagination"]//a[text()="»"]')
        next_page.click()
else:
    read_page()

driver.quit()
