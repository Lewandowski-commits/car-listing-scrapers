import pandas as pd
import re
import scrapers


# function that when provided a dataframe, parses engine capacities from the dataframe series that contain their names
# examples are: 2.0, 1.6, 330i (looking at you, BMW)

def parse_engine_capacities_from_names(data: pd.DataFrame,
                                       name_col: str = "name",
                                       capacity_col: str = "engine_capacity_denoted"):
    data[capacity_col], data[name_col] = data[name_col].apply(
        lambda x: re.findall("([0-9]\.[0-9])|([0-9]{3}[a-z])", x)), data[
                                             name_col].apply(lambda x: re.sub("([0-9]\.[0-9])|([0-9]{3}[a-z])", "", x))
    data[name_col] = data[name_col].str.strip()
    return data

def parse_makes_and_models_from_names(data: pd.DataFrame,
                                      name_col: str = "name",
                                      make_col: str = "make",
                                      model_col: str = "model"):
    data[make_col] = data[name_col].apply(lambda x: x)
    return data

def car_makes():
    return ["Volkswagen",
           "Opel",
           "BMW",
           "Ford",
           "Audi",
           "Mercedes - Benz",
           "Toyota",
           "Renault",
           "Škoda",
           "Škoda",
           "Peugeot",
           "Citroën",
           "Citroën",
           "Hyundai",
           "Kia",
           "Volvo",
           "Nissan",
           "Seat",
           "Fiat",
           "Mazda",
           "Honda",
           "Suzuki",
           "Mitsubishi",
           "Dacia",
           "Jeep",
           "Chevrolet",
           "Mini",
           "Alfa Romeo",
           "Porsche"]

if __name__ == "__main__":
    data = scrapers.scrape_otomoto()
    print(parse_engine_capacities_from_names(data))
    print(parse_makes_and_models_from_names(data))
