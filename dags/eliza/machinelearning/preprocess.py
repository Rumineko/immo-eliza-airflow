import numpy as np
import pandas as pd
from pandas import DataFrame
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
previous_dir = os.path.dirname(current_dir)
collection_dir = os.path.join(previous_dir, "collection")
scrapy_dir = os.path.join(collection_dir, "scrapy")
data_dir = os.path.join(scrapy_dir, "data")


def load_data(path: str) -> DataFrame:
    # Imports the data from the raw folder and returns as a DataFrame
    newpath = os.path.join(scrapy_dir, path)
    df = pd.read_csv(newpath)
    df.drop_duplicates(subset="ID", inplace=True)
    df.set_index("ID", drop=True, inplace=True)
    return df


def fill_empty_data(df: DataFrame) -> DataFrame:
    # Uses Logical Reasoning to Fill in Empty Data
    df.loc[df["Swimming Pool"].isna(), "Swimming Pool"] = 0
    df.loc[df["Openfire"] == False, "Fireplace Count"] = 0
    df.loc[df["Openfire"] == True, "Fireplace Count"] = (
        df["Fireplace Count"].abs().fillna(1)
    )
    df.loc[df["Terrace"] == False, "Terrace Surface"] = 0
    df.loc[df["Garden Exists"] == False, "Garden Surface"] = 0
    return df


def append_data(df: DataFrame) -> DataFrame:
    # Append new data to the existing data
    postals = pd.read_csv(os.path.join(current_dir, "src", "zipcodes.csv"))
    for postalcode in df["Postal Code"]:
        # Appends Municipality to the DataFrame
        municipality = postals[postals["Postcode"] == postalcode]["Hoofdgemeente"]
        province = postals[postals["Postcode"] == postalcode]["Provincie"]
        # Appends Municipality to the DataFrame. Utilizes a smart fill method to fill in the province, if it is not found in the csv file.
        # It's useful in case there are properties in the dataset from another country, which we have encountered in the past.
        if not municipality.empty:
            df.loc[df["Postal Code"] == postalcode, "Municipality"] = (
                municipality.values[0]
            )
        # Appends Province to the DataFrame. Utilizes a smart fill method to fill in the province, if it is not found in the csv file.
        # Same as the above case.
        if not province.empty:
            df.loc[df["Postal Code"] == postalcode, "Province"] = province.values[0]
    return df


def append_data_singular(df: DataFrame) -> DataFrame:
    # Append new data to the existing data
    postals = pd.read_csv(os.path.join(current_dir, "src", "zipcodes.csv"))
    # Appends Municipality to the DataFrame
    postalcode = df["Postal Code"].values[
        0
    ]  # Access the "Postal Code" column correctly
    province = postals[postals["Postcode"] == postalcode]["Provincie"]
    # Appends Province to the DataFrame. Utilizes a smart fill method to fill in the province, if it is not found in the csv file.
    # Same as the above case.
    if not province.empty:
        df.loc[df["Postal Code"] == postalcode, "Province"] = province.values[0]
    return df


def convert_non_numeric_singular(df: DataFrame) -> DataFrame:
    building_state = {
        "TO_RESTORE": 0,
        "TO_RENOVATE": 1,
        "TO_BE_DONE_UP": 2,
        "GOOD": 3,
        "JUST_RENOVATED": 4,
        "AS_NEW": 5,
    }
    df["State of Building"] = (
        df["State of Building"].map(building_state).fillna(df["State of Building"])
    )

    energy_ratings = {
        "G": 8,
        "F": 7,
        "E": 6,
        "D": 5,
        "C": 4,
        "B": 3,
        "A": 2,
        "A+": 1,
        "A++": 0,
    }
    df["EPC"] = df["EPC"].map(energy_ratings).fillna(df["EPC"])

    kitchen_types = {
        "NOT_INSTALLED": 0,
        "USA_UNINSTALLED": 0,
        "SEMI_EQUIPPED": 1,
        "USA_SEMI_EQUIPPED": 1,
        "INSTALLED": 2,
        "USA_INSTALLED": 2,
        "HYPER_EQUIPPED": 3,
        "USA_HYPER_EQUIPPED": 3,
    }
    df["Kitchen Type"] = (
        df["Kitchen Type"].map(kitchen_types).fillna(df["Kitchen Type"])
    )

    df["Province"] = df["Province"].values[0]

    if df["Type"].values[0] == "APARTMENT":
        df["Type_APARTMENT"] = 1
        df["Type_HOUSE"] = 0
    else:
        df["Type_APARTMENT"] = 0
        df["Type_HOUSE"] = 1

    if df["Province"].values[0] == "ANTWERPEN":
        df["Province_ANTWERPEN"] = 1
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "BRUSSEL":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 1
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "HENEGOUWEN":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 1
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "LIMBURG":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 1
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "LUIK":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 1
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "LUXEMBURG":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 1
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "NAMEN":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 1
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "OOST-VLAANDEREN":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 1
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "VLAAMS-BRABANT":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 1
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "WAALS-BRABANT":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 1
        df["Province_WEST-VLAANDEREN"] = 0
    elif df["Province"].values[0] == "WEST-VLAANDEREN":
        df["Province_ANTWERPEN"] = 0
        df["Province_BRUSSEL"] = 0
        df["Province_HENEGOUWEN"] = 0
        df["Province_LIMBURG"] = 0
        df["Province_LUIK"] = 0
        df["Province_LUXEMBURG"] = 0
        df["Province_NAMEN"] = 0
        df["Province_OOST-VLAANDEREN"] = 0
        df["Province_VLAAMS-BRABANT"] = 0
        df["Province_WAALS-BRABANT"] = 0
        df["Province_WEST-VLAANDEREN"] = 1

    df.drop(["Province", "Type"], axis=1, inplace=True)

    boolean = {False: 0, True: 1}
    df["Openfire"] = df["Openfire"].map(boolean).fillna(df["Openfire"])
    df["Furnished"] = df["Furnished"].map(boolean).fillna(df["Furnished"])

    return df


def convert_non_numeric(df: DataFrame) -> DataFrame:
    # Receives a DataFrame and converts non-numeric data to numeric data.
    building_state = {
        "TO_RESTORE": 0,
        "TO_RENOVATE": 1,
        "TO_BE_DONE_UP": 2,
        "GOOD": 3,
        "JUST_RENOVATED": 4,
        "AS_NEW": 5,
    }
    df["State of Building"] = df["State of Building"].apply(
        lambda x: building_state.get(x, np.NAN)
    )

    energy_ratings = {
        "G": 8,
        "F": 7,
        "E": 6,
        "D": 5,
        "C": 4,
        "B": 3,
        "A": 2,
        "A+": 1,
        "A++": 0,
    }
    df["EPC"] = df["EPC"].apply(lambda x: energy_ratings.get(x, np.NAN))

    kitchen_types = {
        "NOT_INSTALLED": 0,
        "USA_UNINSTALLED": 0,
        "SEMI_EQUIPPED": 1,
        "USA_SEMI_EQUIPPED": 1,
        "INSTALLED": 2,
        "USA_INSTALLED": 2,
        "HYPER_EQUIPPED": 3,
        "USA_HYPER_EQUIPPED": 3,
    }
    df["Kitchen Type"] = df["Kitchen Type"].apply(
        lambda x: kitchen_types.get(x, np.NAN)
    )

    boolean = {False: 0, True: 1}

    df["Furnished"] = df["Furnished"].apply(lambda x: boolean.get(x, np.NAN))
    df["Openfire"] = df["Openfire"].apply(lambda x: boolean.get(x, np.NAN))
    return df


def convert_non_numeric_to_numeric(df: DataFrame) -> DataFrame:
    # Receives a DataFrame and converts non-numeric data to numeric data.
    building_state = {
        "TO_RESTORE": 0,
        "TO_RENOVATE": 1,
        "TO_BE_DONE_UP": 2,
        "GOOD": 3,
        "JUST_RENOVATED": 4,
        "AS_NEW": 5,
    }
    df["State of Building"] = df["State of Building"].apply(
        lambda x: building_state.get(x, np.NAN)
    )

    energy_ratings = {
        "G": 8,
        "F": 7,
        "E": 6,
        "D": 5,
        "C": 4,
        "B": 3,
        "A": 2,
        "A+": 1,
        "A++": 0,
    }
    df["EPC"] = df["EPC"].apply(lambda x: energy_ratings.get(x, np.NAN))

    kitchen_types = {
        "NOT_INSTALLED": 0,
        "USA_UNINSTALLED": 0,
        "SEMI_EQUIPPED": 1,
        "USA_SEMI_EQUIPPED": 1,
        "INSTALLED": 2,
        "USA_INSTALLED": 2,
        "HYPER_EQUIPPED": 3,
        "USA_HYPER_EQUIPPED": 3,
    }
    df["Kitchen Type"] = df["Kitchen Type"].apply(
        lambda x: kitchen_types.get(x, np.NAN)
    )

    boolean = {False: 0, True: 1}

    df["Kitchen"] = df["Kitchen"].apply(lambda x: boolean.get(x, np.NAN))
    df["Furnished"] = df["Furnished"].apply(lambda x: boolean.get(x, np.NAN))
    df["Openfire"] = df["Openfire"].apply(lambda x: boolean.get(x, np.NAN))
    df["Terrace"] = df["Terrace"].apply(lambda x: boolean.get(x, np.NAN))
    df["Garden Exists"] = df["Garden Exists"].apply(lambda x: boolean.get(x, np.NAN))
    df["Swimming Pool"] = df["Swimming Pool"].apply(lambda x: boolean.get(x, np.NAN))
    return df


def exclude_outliers(df: DataFrame):
    # Drop the row where Type is not House or Appartment
    df = df[df["Type"].isin(["APARTMENT", "HOUSE"]) | df["Type"].isna()]

    # Drop Kitchen Surface > 100
    df = df[(df["Kitchen Surface"] < 100) | df["Kitchen Surface"].isna()]

    # drop Build year "< 1850"
    df = df[(df["Build Year"] > 1850) | df["Build Year"].isna()]

    # facades <2 -> 2, >4 -> 4
    df["Facades"] = df["Facades"].apply(lambda x: 2 if x < 2 else x)
    df["Facades"] = df["Facades"].apply(lambda x: 4 if x > 4 else x)

    # drop Bathroom Count > 4
    df = df[(df["Bathroom Count"] < 4) | df["Bathroom Count"].isna()]

    # drop bedroom count > 5
    df = df[(df["Bedroom Count"] < 5) | df["Bedroom Count"].isna()]

    # drop colum fireplace count
    df.drop(columns=["Fireplace Count"], inplace=True)

    # drop garden surface > 5000
    df = df[(df["Garden Surface"] < 5000) | df["Garden Surface"].isna()]

    # habitable surface > 700
    df = df[(df["Habitable Surface"] < 700) | df["Habitable Surface"].isna()]

    # drop Landsurface > 3000
    df = df[(df["Land Surface"] < 3000) | df["Land Surface"].isna()]

    # drop the column parking box count
    df.drop(columns=["Parking box count"], inplace=True)

    # drop items with price > 1_000_000
    df = df[(df["Price"] < 1000000) | df["Price"].isna()]

    # drop items that have sale type LIFE_ANNUITY_SALE
    df = df[df["Sale Type"] != "LIFE_ANNUITY_SALE"]

    # only keep items that have SubType == HOUSE, VILLA, TOWN_HOUSE, BUNGALOW, or not specified
    # df = df[df['Subtype'].isin(['HOUSE', 'VILLA', 'TOWN_HOUSE', 'BUNGALOW', None, '']) | df['Subtype'].isna()]

    # only keep items that have toilets of < 6
    df = df[(df["Toilet Count"] < 6) | df["Toilet Count"].isna()]

    return df


def province_to_region(province):
    # This function takes a province as input and returns the region it belongs to
    if province in [
        "LUIK",
        "LIMBURG",
        "WAALS-BRABANT",
        "LUXEMBURG",
        "NAMEN",
        "HENEGOUWEN",
    ]:
        return "Wallonia"
    elif province == "BRUSSEL":
        return "Brussels"
    elif province in [
        "OOST-VLAANDEREN",
        "ANTWERPEN",
        "VLAAMS-BRABANT",
        "WEST-VLAANDEREN",
    ]:
        return "Flanders"
    else:
        return "Unknown"  # For any province value not listed above


def price_per_sqm(df: DataFrame):
    # Create a new column 'Price per Sqm' by dividing the 'Price' column by the 'Habitable Surface', 'Garden Surface' and 'Terrace Surface' columns
    df["Price per sqm"] = df["Price"] / (
        df["Habitable Surface"] + df["Garden Surface"] + df["Terrace Surface"]
    )
    return df


def cleaning():
    time = datetime.now().strftime("%Y-%m-%d")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    previous_dir = os.path.dirname(base_dir)
    collection_dir = os.path.join(previous_dir, "collection")
    scrapy_dir = os.path.join(collection_dir, "scrapy")
    data_dir = os.path.join(scrapy_dir, "data")
    csv = os.path.join(data_dir, f"data_{time}.csv")
    # And Finally, the main function
    # We start off by loading the raw data
    raw_data = load_data(csv)
    # We then append the data
    appended_data = append_data(raw_data)
    # We then convert the non-numeric data to numeric data
    converted_data = convert_non_numeric_to_numeric(appended_data)
    # We then fill in the empty data
    filled_data = fill_empty_data(converted_data)
    # We drop some columns that we don't need
    filled_data.drop(
        columns=[
            "Sewer",
            "Terrace Orientation",
            "Garden Orientation",
            "Has starting Price",
            "Transaction Subtype",
            "Is Holiday Property",
            "Gas Water Electricity",
            "Parking count inside",
            "Parking count outside",
            "Land Surface",
        ],
        inplace=True,
    )
    # We create a new column 'Region' by applying the function 'province_to_region' to the 'Province' column
    filled_data["Region"] = filled_data["Province"].apply(province_to_region)
    # We use the price_per_sqm function to create a new column 'Price per Sqm'
    filled_data = price_per_sqm(filled_data)
    # We output the data to a new csv file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    newpath = os.path.join(current_dir, "data", "cleaned", f"data_{time}.csv")
    filled_data.to_csv(newpath)


if __name__ == "__main__":
    cleaning()
