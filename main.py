from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from tqdm import tqdm

AD_TITLE_COL = "Title"
AD_PRICE_COL = "Price"
AD_DETAILS_KEY = "Details"
CSV_FILE_NAME = "ktmcarsales.csv"

Detail_Column_Names = set([AD_TITLE_COL, AD_PRICE_COL])


def get_page(page_no) -> str:
    url = f'https://www.ktmcarsales.com/buy-cars-kathmandu-nepal/page/{page_no}/'
    return requests.get(url).text


def get_detail_page(car_name_tag) -> dict():
    detail_link = car_name_tag.find('a')["href"]
    html_ = requests.get(detail_link).text
    soup = BeautifulSoup(html_, 'html.parser')
    details = soup.find_all('li', id=re.compile("cp_"))
    details_dict: dict = {}
    for detail in details:
        if ": " in detail.text:
            key, value = detail.text.split(": ")
            Detail_Column_Names.add(key)
            details_dict[key] = value

    return details_dict


def get_ad_data(soup) -> list:
    postblocks = soup.find_all('div', class_='post-block')
    page_data_list = []
    for postblock in postblocks:
        car_data_dict = {}
        car_name_h3_tag = postblock.find('h3')
        car_name = car_name_h3_tag.text
        car_price = postblock.find('p', class_='post-price').text
        car_data_dict[AD_TITLE_COL] = car_name
        car_data_dict[AD_PRICE_COL] = car_price
        car_data_dict = dict(car_data_dict, **get_detail_page(car_name_h3_tag))
        page_data_list.append(car_data_dict)

    return page_data_list


def get_last_pageNo(soup) -> int:
    pages_numbers = soup.find_all(
        'a', class_="page-numbers")
    return int(pages_numbers[-2].text)


def save_to_csv(data):
    print("Saving...\n")
    df = pd.DataFrame.from_dict(data)
    df.to_csv(f"./{CSV_FILE_NAME}")
    print("Saved!!!!")


def main():
    page_no: int = 1
    data = []
    soup = BeautifulSoup(get_page(page_no), 'html.parser')
    last_page_no: int = get_last_pageNo(soup)
    data = [*data, *get_ad_data(soup)]

    for page_no in tqdm(range(2, last_page_no+1), desc="Scrapping...", ascii=False, ncols=75):
        soup = BeautifulSoup(get_page(page_no), 'html.parser')
        data = [*data, *get_ad_data(soup)]

    print("Scrapping Completed!!!\n")

    save_to_csv(data)


if __name__ == "__main__":
    main()
