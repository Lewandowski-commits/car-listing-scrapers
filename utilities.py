import pandas as pd
import re
import Polish


# function that when provided a dataframe, parses engine capacities from the dataframe series that contain their names
# examples are: 2.0, 1.6, 330i (looking at you, BMW)

def parse_engine_capacities_from_names(data: pd.DataFrame, name_col: str = "name",
                                       capacity_col: str = "engine_capacity_denoted"):
    data[capacity_col], data[name_col] = data[name_col].apply(
        lambda x: re.findall("([0-9]\.[0-9])|([0-9]{3}[a-z])", x)), data[
                                             name_col].apply(lambda x: re.sub("([0-9]\.[0-9])|([0-9]{3}[a-z])", "", x))
    data[name_col] = data[name_col].str.strip()
    return data


if __name__ == "__main__":
    print(parse_engine_capacities_from_names(Polish.scrape_otomoto()))
