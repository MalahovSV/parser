import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
import datetime


time_dict = {
             "2": "08:50",
             "3": "09:45",
             "4": "10:40"
}

def authorization(browser, login, password):
    inputs = browser.find_elements(By.TAG_NAME, "input")
    time.sleep(1)
    buttons = browser.find_elements(By.TAG_NAME, "button")
    time.sleep(1)
    inputs[2].send_keys(login)
    inputs[3].send_keys(password)
    time.sleep(1)
    print(f"Логин: {login}\nПароль: {'•'*len(password)}")
    buttons[1].click()

def get_disciplines(browser):
    time.sleep(4)
    result = {}
    rows = browser.find_elements(By.XPATH, "//tbody//tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        #0 - Добавить, 1 - Список
        a_href = cells[4].find_elements(By.TAG_NAME, 'a')[0].get_attribute("href")
        result[f'{cells[2].text} {cells[1].text}'] = a_href
    return result

def set_record(browser, _date, _time, _lesson, _room, _class, _teacher):
        time.sleep(1)
        type_work =  Select(browser.find_element(By.NAME, "control_type_id"))
        date_field = browser.find_element(By.NAME, "date")
        time_field = browser.find_element(By.NAME, "time")
        lesson_field = browser.find_element(By.NAME, "lesson_number")
        room_field = browser.find_element(By.NAME, "room_number")
        class_field = browser.find_element(By.NAME, "cluster_name")
        teacher_field = browser.find_element(By.NAME, "teacher_name")
        type_work.select_by_value("1")
        browser.execute_script(f"arguments[0].value = '{_date}';", date_field)
        time_field.send_keys(f"{_time}")
        lesson_field.send_keys(f"{_lesson}") #2/3/4
        room_field.send_keys(f"{_room}")
        class_field.send_keys(f"{_class}")
        teacher_field.send_keys(f"{_teacher}")
        time.sleep(1)
        save_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Сохранить')]")
        save_button.click()


if __name__ == "__main__":
    with open('data') as data:
        login, password, url = data.read().split()

    try:
        browser = webdriver.Chrome()
        browser.get(url)
        authorization(browser, login, password)
        disciplines = get_disciplines(browser)
        
        # Чтение Excel-файла
        df = pd.read_excel("data.xlsx")
        # Проходим по каждой строке
        for index, row in df.iterrows():
            print("-" * 50)
            browser.get(disciplines[f"{row['Предмет']} {row['Класс']}"])
            set_record(browser, 
                       str(row['Дата'])[:-9], 
                       time_dict[str(row['Номер урока'])],
                       row['Номер урока'],
                       row['Кабинет'],
                       f"{row['Класс']}{row['Литера']}",
                       row['Учитель'])
            
            print(f"✅ Заполнено: {row["Предмет"]} {str(row['Дата'])[:-9]} | {time_dict[str(row['Номер урока'])]} | {row['Номер урока']} | {row['Кабинет']} | {row['Класс']}{row['Литера']} | {row['Учитель']}")
            time.sleep(1)
            browser.get(url)

    except ValueError as err:
         print("Сведения об ошибке:", err)

    finally:
         browser.quit()

    