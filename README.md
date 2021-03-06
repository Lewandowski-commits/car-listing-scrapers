# car-listing-scrapers
Python functions that return dataframes containing car listings from provided links.

## Prerequisites & packages
The following packages are required to be preinstalled to run this notebook: 
- pandas
- requests
### Package installation
If you are missing any of the above packages, you can install them from your Python console using the following command:
```
pip install <package name>
```
It also uses the following built-in packages that should be included in your Python distribution:
- re
## Use
### Polish.py
#### Supported sites
- otomoto.pl
- olx.pl
- mobile.de

Import the module into your .py file and run any of its functions with a link to the search results from a specific website in order to scrape it into a Pandas dataframe. 

If no argument is passed in, a default link will be used. All functions will default to a 2006+ Hyundai Coupe just for reference.
```
scrape_otomoto("https://www.otomoto.pl/osobowe/hyundai/coupe/od-2006/")
scrape_olx("https://www.olx.pl/motoryzacja/samochody/hyundai/coupe/?search%5Bfilter_float_year%3Afrom%5D=2006&view=list")
scrape_mobile("https://suchen.mobile.de/fahrzeuge/search.html?dam=0&fr=2006%3A&isSearchRequest=true&ms=11600%3B4%3B%3B%3B&s=Car&sfmr=false&vc=Car")
```

You can also use the below function and pass in any link - it will determine the right function to use for scraping.
```
smart_scrape(any of search result URLs from the supported sites)
```

### utils.py
Import to use helpful utility functions when working with the scraped dataframes. 

## Todo
- Add support for other sites
  - Polish
    - allegro.pl
    - allegrolokalnie.pl
   - EU-wide
      - autoscout
    - ...and more
