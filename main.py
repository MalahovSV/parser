import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def authorization(browser, login, password):
    inputs = browser.find_elements(By.TAG_NAME, "input")
    buttons = browser.find_elements(By.TAG_NAME, "button")
    inputs[2].send_keys(login)
    inputs[3].send_keys(password)
    print(f"Логин: {login}\nПароль: {password}")
    buttons[1].click()
    time.sleep(125)



if __name__ == "__main__":
    with open('data') as data:
        login, password, url = data.read().split()
    with webdriver.Chrome() as browser:
        wait = WebDriverWait(browser, 10)  # Увеличил время ожидания
        browser.get(url)
        authorization(browser, login, password)

'''
    for element in buttons:
        field_type = element.get_attribute('type')
        field_name = element.get_attribute('name')
        field_id = element.get_attribute('id')
        field_class = element.get_attribute('class')
        print(f"FIELD_TYPE: {field_type}        FILED_NAME: {field_name}, FIELD_ID: {field_id}, FIELD_CLASS: {field_class}\n\n\n")
''' 
