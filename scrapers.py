# import libraries
import requests
import pandas as pd
import numpy as np
import bs4
from bs4 import BeautifulSoup
from pandas import DataFrame
import re
from datetime import datetime


# define the scraping function for otomoto.pl
# function will only work if a search results link is passed in
# i.e. "https://www.otomoto.pl/osobowe/hyundai/coupe/od-2006/"
def scrape_otomoto(search_url: str = "https://www.otomoto.pl/osobowe/hyundai/coupe/od-2006/"):
    # access the link
    res = requests.get(search_url)
    res.raise_for_status()

    # create the BS object
    carSoup = BeautifulSoup(res.text, features='lxml')

    # check how many pages are there to later loop over
    try:
        lastPage = int(carSoup.select('.page')[-1].text)
    except:
        lastPage = 1

    # create the dict upon which the dataframe will be built
    d = {'name': [],
         'year': [],
         'price': [],
         'currency': [],
         'mileage (km)': [],
         'fuel type': [],
         'disp (cm3)': [],
         'city': [],
         'link': []}

    # Loop over all the pages, load them, get the list of all car
    for page in range(1, lastPage + 1):

        # check if the links need to be modified when looping over
        if lastPage > 2:
            res = requests.get(search_url + '&page=' + str(page))
        else:
            res = requests.get(search_url)

        # access the link
        res.raise_for_status()

        # create the BS object and select all listings
        currentPage = BeautifulSoup(res.text, features='lxml')
        carList = currentPage.select('article.offer-item')

        # loop over all  listings on the page
        for car in carList:

            # scrape as much information from the listings as possible and put them in the dictionary

            d['name'].append(
                car.find('a', class_='offer-title__link').get('title'))

            d['year'].append(
                int(re.sub('[^0-9]', '', car.find('li', {'data-code': 'year'}).text)))

            d['link'].append(
                car.find('a')['href'])

            d['price'].append(
                float(car.find('span', class_='offer-price__number ds-price-number').find('span').text.replace(' ',
                                                                                                               '').replace(
                    ',', '.')))

            d['currency'].append(
                car.find('span', class_='offer-price__currency ds-price-currency').text)

            # mileage isn't a mandatory field to fill, so check if it's present and then append as necessary
            if isinstance(car.find('li', {'data-code': 'mileage'}), bs4.element.Tag):
                d['mileage (km)'].append(
                    int(re.sub('[^0-9]', '', car.find('li', {'data-code': 'mileage'}).text)))
            else:
                d['mileage (km)'].append(np.NaN)

            d['fuel type'].append(
                car.find('li', {'data-code': 'fuel_type'}).text.replace('\n', ''))

            # displacement isn't a mandatory field to fill, so check if it's present and then append as necessary
            if isinstance(car.find('li', {'data-code': 'engine_capacity'}), bs4.element.Tag):
                d['disp (cm3)'].append(float((
                    re.sub('(\n)|(cm3)|', '', car.find('li', {'data-code': 'engine_capacity'}).text.replace(' ', '')))))
            else:
                d['disp (cm3)'].append(np.NaN)

            d['city'].append(
                car.find('span', class_='ds-location-city').text)

        print('Parsed page {} of {} otomoto.pl'.format(str(page), str(lastPage)))

    # create the dataframe object and return it
    df_otomoto = DataFrame({key: pd.Series(value) for key, value in d.items()})

    df_otomoto.drop_duplicates(inplace=True)

    return df_otomoto


def scrape_olx(search_url: str = "https://www.olx.pl/motoryzacja/samochody/hyundai/coupe/?search%5Bfilter_float_year%3Afrom%5D=2006&view=list"):
    # access the link
    res = requests.get(search_url)
    res.raise_for_status()

    # create the BS object
    carSoup = BeautifulSoup(res.text, features='lxml')

    # check how many pages are there to later loop over
    try:
        lastPage = int(carSoup.findAll("a", class_="block br3 brc8 large tdnone lheight24")[-1].text)
    except:
        lastPage = 1

    print(lastPage)

    # create the dict upon which the dataframe will be built
    d = {'name': [],
         'year': [],
         'price': [],
         'currency': [],
         'mileage (km)': [],
         'fuel type': [],
         'disp (cm3)': [],
         'city': [],
         'link': []}

    # Loop over all the pages, load them, get the list of all car
    for page in range(1, lastPage + 1):

        # check if the links need to be modified when looping over
        if lastPage > 2:
            res = requests.get(search_url + '&page=' + str(page))
        else:
            res = requests.get(search_url)

        # access the link
        res.raise_for_status()

        # create the BS object and select all listings
        currentPage = BeautifulSoup(res.text, features='lxml')
        carList = currentPage.find_all("div", class_="offer-wrapper")

        # loop over all  listings on the page
        for car in carList:

            # scrape as much information from the listings as possible and put them in the dictionary

            d['name'].append(
                car.find_all('strong')[0].text)

            d['link'].append(
                car.find('a')['href'])

            d['price'].append(
                float(car.find_all('strong')[1].text.replace("zł", "").replace(" ", "").strip()))

            d['currency'].append("PLN")

            d['city'].append(
                car.find_all("tr")[-1].find('span').text)

        print('Parsed page {} of {} olx.pl'.format(str(page), str(lastPage)))

    # create the dataframe object and return it
    df_olx = DataFrame({key: pd.Series(value) for key, value in d.items()})

    df_olx.drop_duplicates(inplace=True)

    return df_olx


if __name__ == "__main__":
    currtime = datetime.now().strftime('D%d-%m-%Y T%H-%M-%S')

    try:
        joint_results = scrape_otomoto(input("Please provide otomoto.pl search results link: ")).append(
            scrape_olx(input("Please provide olx.pl search results link: "))
        )
        joint_results.to_csv(f"data/{currtime}.csv", index=False)
        print("Success!")
    except:
        print("Failed!")
    finally:
        print("Exiting!")
