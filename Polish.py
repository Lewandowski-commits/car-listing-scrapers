# import libraries
import requests
import pandas as pd
import numpy as np
import bs4
from bs4 import BeautifulSoup
from pandas import DataFrame
import re


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

        print('Parsed page {} of {}'.format(str(page), str(lastPage)))

    # create the dataframe object and return it
    df_otomoto = DataFrame({key: pd.Series(value) for key, value in d.items()})

    df_otomoto.drop_duplicates(inplace=True)

    return df_otomoto


if __name__ == "__main__":
    try:
        print(scrape_otomoto())
        print("Success!")
    except:
        print("Failed!")
    finally:
        print("Exiting!")
