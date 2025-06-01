from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import StaleElementReferenceException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

button_ids = [
    "buyCursor",
    "buyGrandma",
    "buyFactory",
    "buyMine",
    "buyShipment",
    "buyAlchemy lab",
    "buyPortal",
    "buyTime machine",
]

def update_money():
    money = driver.find_element(By.CSS_SELECTOR, "div #money").text.replace(",", "")

    return int(money)

def update_cost():
    all_prices = [
        int(item.text.split(' - ')[1].replace(",", ""))
        for item in driver.find_elements(By.CSS_SELECTOR, '#store b')
        if ' - ' in item.text
    ]

    item_prices = {i: {button_id: price} for i, (button_id, price) in enumerate(zip(button_ids, all_prices))}

    return item_prices

def cookie_clicker():
    start_time = time.time()

    while time.time() - start_time < 10:
        try:
            driver.find_element(By.CSS_SELECTOR, "div #cookie").click()
        except StaleElementReferenceException:
            continue

def check_upgrades():
    for idx in range(7, -1, -1):

        money = update_money()

        try:
            item_prices = update_cost()
        except StaleElementReferenceException:
            print(f"Stale element in update_cost at index {idx}, skipping...")
            continue

        if item_prices[idx][button_ids[idx]] < money:
            try:
                driver.find_element(By.ID, button_ids[idx]).click()
            except StaleElementReferenceException:
                print(f"Stale element in check_upgrades at index {idx}, skipping...")
                continue

game_start_time = time.time()

while time.time() - game_start_time < 300:
    cookie_clicker()
    check_upgrades()

print(f'\nCookies/second: {driver.find_element(By.CSS_SELECTOR, "div #cps").text.split(" ")[2]}')
driver.close()