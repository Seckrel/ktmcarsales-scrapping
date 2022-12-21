from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import requests
import re


# def get_page(driver, page_no) -> str:
#     url = f'https://www.ktmcarsales.com/buy-cars-kathmandu-nepal/page/{page_no}/'
#     driver.get(url)
#     return driver.page_source

def get_page(page_no) -> str:
    url = f'https://www.ktmcarsales.com/buy-cars-kathmandu-nepal/page/{page_no}/'
    html_ = requests.get(url).text
    return  html_


def get_detail_page(car_name_tag):
    detail_link = car_name_tag.find('a')["href"]
    html_ = requests.get(detail_link).text
    soup = BeautifulSoup(html_, 'html.parser')
    details = soup.find_all('li', id=re.compile("cp_"))
    for detail in details:
        detail_info, value = detail.text.split(": ")
        print(f"{detail_info} = {value}")


def hit_elements_soup(soup) -> None:
    postblocks = soup.find_all('div', class_='post-block')
    for postblock in postblocks:
        car_name_h3_tag = postblock.find('h3')
        car_name = car_name_h3_tag.text
        car_price = postblock.find('p', class_='post-price').text
        print(f'''
        Car Name: {car_name}
        Car price: {car_price}
        '''
              )
        get_detail_page(car_name_a_tag)
        break


def get_last_pageNo(soup) -> int:
    pages_numbers = soup.find_all(
        'a', class_="page-numbers")
    print(pages_numbers)
    return int(pages_numbers[-2].text)


options = Options()
options.headless = True


def main():
    page_no: int = 1
    soup = BeautifulSoup(get_page(page_no), 'html.parser')
    last_page_no: int = get_last_pageNo(soup)
    hit_elements_soup(soup)
    for page_no in range(2, last_page_no+1):
        soup = BeautifulSoup(get_page(page_no), 'html.parser')
        hit_elements_soup(soup)
        if page_no == 3:
            break


# with webdriver.Firefox(options=options) as driver:
#     page_no: int = 1
#     soup = BeautifulSoup(get_page(driver, page_no), 'html.parser')
#     last_page_no: int = get_last_pageNo(soup)
#     hit_elements_soup(soup)
#     # for page_no in range(2, last_page_no+1):
#     #     soup = BeautifulSoup(get_page(driver, page_no), 'html.parser')
#     #     hit_elements_soup(soup)

# driver.implicitly_wait(10)

if __name__ == "__main__":
    main()
