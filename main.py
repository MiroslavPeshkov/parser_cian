import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from shutil import which
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openpyxl
import xlsxwriter
from PIL import Image

firefoxOptions = Options()
FIREFOXPATH = which("firefox")
# firefoxOptions.add_argument('--headless')
firefoxOptions.add_argument('--no-sandbox')
firefoxOptions.add_argument("--window-size=1920,1080")
firefoxOptions.add_argument('--disable-dev-shm-usage')
firefoxOptions.add_argument('--ignore-certificate-errors')
firefoxOptions.add_argument('--allow-running-insecure-content')
firefoxOptions.binary = FIREFOXPATH

"""

ПАПКИ
screen_house - скрины домов
screen_plot - скрины участков
screenshots - скрины заданных в консоли адреса

"""
PATH_FIREFOX = './geckodriver'


def get_screen(input_geo, name):
    URLs_Yandex = "https://yandex.ru/maps/"
    browser = webdriver.Firefox(executable_path=PATH_FIREFOX, options=firefoxOptions)
    browser.get(URLs_Yandex)
    time.sleep(2)

    input_text = browser.find_element(By.XPATH, "//input[@type='text']")
    input_text.send_keys(input_geo)
    input_text.send_keys(Keys.ENTER)
    time.sleep(5)

    # close_pop_up = browser.find_element(By.XPATH, "//button[@aria-label='Закрыть']")
    # action = ActionChains(browser)
    # action.move_to_element(close_pop_up).click().perform()


    close_win_left = browser.find_element(By.XPATH, "//span[@class='inline-image _loaded sidebar-toggle-button__icon']")
    browser.execute_script("arguments[0].click();", close_win_left)

    time.sleep(2)

    # close_pop_up = browser.find_element(By.XPATH, "//button[@class='button _view_secondary-blue _ui _size_small']")
    # browser.execute_script("arguments[0].click();", close_pop_up)

    time.sleep(1)

    min_zoom = browser.find_element(By.XPATH, "//button[@aria-label='Отдалить']")

    for i in range(4): # Здесь идет отдаление от карты, чтобы уменьшить нужно сделать for i in range(3)
        min_zoom.click()
        time.sleep(1)
    time.sleep(1)
    browser.save_screenshot(f'./screenshots/Аналог{name}_min.png')

    time.sleep(4)

    for i in range(3): # Здесь идет отдаление от карты, чтобы уменьшить нужно сделать for i in range(3)
        min_zoom.click()
        time.sleep(1)
    time.sleep(2)
    browser.save_screenshot(f'./screenshots/Аналог{name}_max.png')
    browser.quit()


def get_info_house(URLs):
    browser = webdriver.Firefox(executable_path=PATH_FIREFOX, options=firefoxOptions)
    count = 0
    dict_house = {}
    for URL in URLs:
        count += 1

        browser.get(URL)

        count_house = f'Аналог {count}'

        time.sleep(2)


        try:
            active = browser.find_element(By.XPATH,"//div[@data-name='OfferUnpublished']")
            if active:
                active = "Не активна"
                dict_house[count_house] = {

                    'Информация, опубликованная на сайте': URL,
                    "Адрес": None,
                    "Шоссе": None,
                    "Расстояние от МКАД, км.": None,
                    "Дата предложения/продажи": None,
                    "Характеристика земельного участка": None,
                    "Площадь земельного участка кв.м.": None,
                    "Категория земель": None,
                    "Вид разрешенного использования": None,
                    "Передаваемые права на земельный участок": None,
                    "Газ": None,
                    "Вода центральная": None,
                    "Электроснабжение": None,
                    "Канализация": None,
                    "Отопление": None,
                    "Коммуникации": None,
                    "Наличие типовых дополнительных улучшений": None,
                    "Наличие мебели": None,
                    "Благоустройство участка": None,
                    "Характеристика улучшений земельного участка": None,
                    "Назначение": None,
                    "Площадь дома кв.м.": None,
                    "Этажность": None,
                    "Материалы стен": None,
                    "Состояние жилого дома": None,
                    "Состояние внутренней отделки": None,
                    "Отделка фасада": None,
                    "Передаваемые права на улучшение учатска": None,
                    "Цена предложения (окс+зу). руб.": None,
                    'Активность объявления': active

                }
                continue
        except:
            active = "Активна"

        print('active ---> ', active)


        try:
            close_pop = browser.find_elements(By.XPATH, "//button[@type='button']")[-1]
            browser.execute_script("arguments[0].click();", close_pop)

            but_num = browser.find_elements(By.XPATH, "//span[text()[contains(., 'Показать телефон')]]")[-1]
            browser.execute_script("arguments[0].click();", but_num)
        except:
            pass
        time.sleep(2)

        pattern_sq = re.compile(r'\d+')

        try:
            name = browser.find_element(By.XPATH, "//h1").text

            time.sleep(2)
        except:
            name = None


        browser.execute_script("window.scrollTo(0, 300)")
        time.sleep(3)
        browser.save_screenshot(f"./screen_house/Аналог {count} first.png")

        try:
            total_price = browser.find_element(By.XPATH, "//span[@itemprop='price']").text.replace('₽', '').strip().replace(' ',
                                                                                                                        '')
        except:
            total_price = None

        # print('total_price', total_price)
        try:
            geo = browser.find_element(By.XPATH, "//div[@data-name='Geo']/span").get_attribute('content')

        except:
            geo = None
        # print('geo', geo)

        try:
            high_way = browser.find_elements(By.XPATH, "//div[@data-name='Geo']//following-sibling::ul")[-1].text
            high_way_ = high_way.split(',')[0].strip().replace('шоссе', '').strip()
        except:
            high_way = None
            high_way_ = None
        # print('high_way', high_way_)

        try:
            dist_from_mkad = re.findall(pattern_sq, high_way)  # regex

            if len(dist_from_mkad) > 0:
                dist_from_mkad = dist_from_mkad[0]
            else:
                dist_from_mkad = None
        except:
            dist_from_mkad = None

        # print('dist_from_mkad', dist_from_mkad)

        try:
            squared = browser.find_element(By.XPATH, "//div[text()[contains(., 'Участок')]]//preceding-sibling::div").text
            pattern_squared_house = re.compile("[а-яА-Я]")
            squared = re.sub(pattern_squared_house, '', squared)
            squared = squared.strip('.').strip()
            squared = float(squared) * 100
        except:
            squared = None

        try:
            pattern_sq_ = re.compile(r'\s\d+\S+')
            squared_house = re.findall(pattern_sq_, name)  # regex
            """
            TODO
            """
            if len(squared_house) > 0:
                squared_house = squared_house[0].strip()
                squared_house = re.sub(pattern_squared_house, '', squared_house)
            else:
                squared_house = None
        except:
            squared_house = None

        # print('squared_house', squared_house)

        try:
            floors_house = browser.find_element(By.XPATH,
                                            "//div[text()[contains(., 'Этажей в доме')]]//preceding-sibling::div").text
        except:
            floors_house = None

        try:
            element = browser.find_element(By.XPATH, "//div[text()[contains(., 'Общая информация')]]")
            browser.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(3)
        except:
            browser.execute_script("window.scrollTo(0, 1100)")
            time.sleep(3)

        browser.save_screenshot(f"./screen_house/Аналог {count} second.png")


        dict_house[count_house] = {

            'Информация, опубликованная на сайте': URL,
            "Адрес": geo,
            "Шоссе": high_way_,
            "Расстояние от МКАД, км.": dist_from_mkad,
            "Дата предложения/продажи": None,
            "Характеристика земельного участка": None,
            "Площадь земельного участка кв.м.": squared,
            "Категория земель": None,
            "Вид разрешенного использования": None,
            "Передаваемые права на земельный участок": None,
            "Газ": None,
            "Вода центральная": None,
            "Электроснабжение": None,
            "Канализация": None,
            "Отопление": None,
            "Коммуникации": None,
            "Наличие типовых дополнительных улучшений": None,
            "Наличие мебели": None,
            "Благоустройство участка": None,
            "Характеристика улучшений земельного участка": None,
            "Назначение": None,
            "Площадь дома кв.м.": squared_house,
            "Этажность": floors_house,
            "Материалы стен": None,
            "Состояние жилого дома": None,
            "Состояние внутренней отделки": None,
            "Отделка фасада": None,
            "Передаваемые права на улучшение учатска": None,
            "Цена предложения (окс+зу). руб.": total_price,
            'Активность объявления' : active

        }

    browser.quit()

    return dict_house

def get_info_plot(URLs):
    browser = webdriver.Firefox(executable_path=PATH_FIREFOX, options=firefoxOptions)
    count = 0
    dict_plot = {}
    for URL in URLs:
        count += 1
        browser.get(URL)

        count_house = f'Аналог {count}'

        time.sleep(2)
        print('=='*500)

        try:
            active = browser.find_element(By.XPATH, "//div[@data-name='OfferUnpublished']")
        except:
            active = None

        if active:
            active = "Не активна"
            dict_plot[count_house] = {
                "Информация, опубликованная на сайте": URL,
                "Адрес": None,
                "Шоссе": None,
                "Расстояние от МКАД, км": None,
                "Дата предложения/продажи": None,
                "Площадь земельного участка кв.м.": None,
                "Категория земель": None,
                "Назначение": None,
                "Передаваемые права на земельный участок": None,
                "Коммуникации": None,
                "Наличие ветхих строений": None,
                "Наличие лесного массива на участке": None,
                "Подъезд": None,
                "Цена предложеня": None,
                'Активность объявления': active
            }
        else:

            print('active ---> ', active)
            try:

                close_pop = browser.find_elements(By.XPATH, "//button[@type='button']")[-1]
                browser.execute_script("arguments[0].click();", close_pop)

                but_num = browser.find_elements(By.XPATH, "//span[text()[contains(., 'Показать телефон')]]")[-1]
                browser.execute_script("arguments[0].click();", but_num)
            except:
                pass


            browser.execute_script("window.scrollTo(0, 300)")
            time.sleep(1)
            browser.save_screenshot(f"./screen_plot/Аналог {count} first.png")

            try:
                geo = browser.find_element(By.XPATH, "//div[@data-name='Geo']/span").get_attribute('content')

            except:
                geo = None
            print('geo', geo)

            try:
                total_price = browser.find_element(By.XPATH, "//span[@itemprop='price']").text.replace('₽', '').strip().replace(' ',
                                                                                                                            '')
            except:
                total_price = None

            print('total_price', total_price)

            try:
                high_way = browser.find_elements(By.XPATH, "//div[@data-name='Geo']//following-sibling::ul")[-1].text
                high_way_ = high_way.split(',')[0].strip().replace('шоссе', '').strip()
            except:
                high_way = None
                high_way_ = None
            print('high_way', high_way_)

            try:
                pattern_sq = re.compile(r'\d+')
                dist_from_mkad = re.findall(pattern_sq, high_way)  # regex

                if len(dist_from_mkad) > 0:
                    dist_from_mkad = dist_from_mkad[0]
                else:
                    dist_from_mkad = None
            except:
                dist_from_mkad = None

            print('dist_from_mkad', dist_from_mkad)

            try:
                squared = browser.find_element(By.XPATH, "//div[text()[contains(., 'Площадь')]]//preceding-sibling::div").text
                pattern_squared_house = re.compile("[а-яА-Я]")
                squared = re.sub(pattern_squared_house, '', squared)
                squared = squared.strip('.')
            except:
                squared = None

            print('squared  ', squared)
            try:
                status = browser.find_element(By.XPATH, "//div[text()[contains(., 'Статус земли')]]//preceding-sibling::div").text

                if status == "Дачное некоммерческое партнерство":
                    status = 'ДНП'
                else:
                    status = status
            except:
                status = None
            print('status  ', status)

            try:
                element = browser.find_element(By.XPATH, "//div[text()[contains(., 'Общая информация')]]")
                browser.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(1)
            except:
                browser.execute_script("window.scrollTo(0, 1100)")
                time.sleep(1)


            browser.save_screenshot(f"./screen_plot/Аналог {count} second.png")

            dict_plot[count_house] = {

                        "Информация, опубликованная на сайте": URL,
                        "Адрес": geo,
                        "Шоссе": high_way_,
                        "Расстояние от МКАД, км": dist_from_mkad,
                        "Дата предложения/продажи": None,
                        "Площадь земельного участка кв.м.": squared,
                        "Категория земель": None,
                        "Назначение": status,
                        "Передаваемые права на земельный участок": None,
                        "Коммуникации": None,
                        "Наличие ветхих строений": None,
                        "Наличие лесного массива на участке": None,
                        "Подъезд": None,
                        "Цена предложеня": total_price,
                        'Активность объявления': active
            }
    return dict_plot

def create_excel(dict_house, dict_plot):
    df = pd.DataFrame.from_dict(dict_house)
    df = df.reset_index()
    df = df.rename(columns={'index': 'Показатель'})
    df1 = pd.DataFrame.from_dict(dict_plot)
    df1 = df1.reset_index()
    df1 = df1.rename(columns={'index': 'Показатель'})
    path = "/Users/miroslav/PycharmProjects/cian/excel/Data.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Расчет ДОМ')
    df1.to_excel(writer, sheet_name='Расчет УЧАСТОК')
    writer.close()

def crop(png_image_name):
    if 'max' in png_image_name:
        im = Image.open(png_image_name)
        img_left_area = (1000, 150, 1900, 1800)

        img_left = im.crop(img_left_area)
        img_left.save(png_image_name)

    if 'min' in png_image_name:
        im = Image.open(png_image_name)
        img_left_area = (100, 100, 2000, 2200)

        img_left = im.crop(img_left_area)
        img_left.save(png_image_name)

if __name__ == '__main__':

    # Здесь задаются ссылки на циан объекты - дома
    URLs_house = [
        "https://solnechnogorsk.cian.ru/sale/suburban/279724685/",
        "https://solnechnogorsk.cian.ru/sale/suburban/280012567/",
        "https://solnechnogorsk.cian.ru/sale/suburban/279798420/",
        "https://solnechnogorsk.cian.ru/sale/suburban/277959586/"
    ]
    # Здесь задаются ссылки на циан объекты - участки
    URLs_plot = [
        "https://solnechnogorsk.cian.ru/sale/suburban/257665456/",
        "https://solnechnogorsk.cian.ru/sale/suburban/270034701/",
        "https://solnechnogorsk.cian.ru/sale/suburban/273553299/"
    ]

    # Вводится адрес необходимого скриншота
    adress = input('Введите адрес: ')
    count = input('Введите порядковый номер, который будет уникален для адреса скришота: ')

    dict_house = get_info_house(URLs_house)
    dict_plot = get_info_plot(URLs_plot)
    create_excel(dict_house, dict_plot)

    get_screen(adress, count)

    filepath = './excel/Data.xlsx'
    import subprocess, os, platform
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))















