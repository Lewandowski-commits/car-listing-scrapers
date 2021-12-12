import pandas as pd
import re
import scrapers
import json
import requests


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

    api_car_makes = 'https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getMakes'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

    res = requests.get(api_car_makes, headers=headers).text[2:-2]

    car_makes_json = json.loads(res)['Makes']
    car_makes = [x['make_display'] for x in car_makes_json]
    car_makes_id = [x['make_id'] for x in car_makes_json]
    car_makes_country = [x['make_country'] for x in car_makes_json]
    car_makes_df = pd.DataFrame({'id': car_makes_id, 'name': car_makes, 'country': car_makes_country})

    def _parse_makes(input_string, list_to_match):
        result_matches = [x for x in input_string.split() if x in list_to_match]

        return result_matches

    data[make_col] = data[name_col].apply(lambda x: _parse_makes(x, car_makes)).astype('str')
    #result = pd.merge(data,
    #                car_makes_df,
    #                how='left',
    #                left_on=[make_col],
    #                right_on=['name']).fillna(0)

    result = data

    return result


if __name__ == "__main__":
    pass()
