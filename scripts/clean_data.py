# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      clean_data.py                                      ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: Branly, Tran Quoc <->                          ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://github.com/StephaneBranly              +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2022/05/31 18:38:56 by Branly, Tran Quoc   ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import pandas as pd
import pyproj

from .utils import *


def convert_to_latlon(data):
    """
    Transform the dataframe to add a latitude and longitude column for each row, eventually calculated from other columns
    """
    bng = pyproj.Proj("epsg:27700")
    wgs84 = pyproj.Proj("epsg:4326")

    for index, row in data.iterrows():
        if pd.isnull(row["latitude"]):
            if row["easting_rounded"]:
                lat, lon = pyproj.transform(
                    bng, wgs84, row["easting_rounded"], row["northing_rounded"]
                )
                data.at[index, "latitude"] = lat
                data.at[index, "longitude"] = lon

    # delete needless features
    for key in ["easting_rounded", "northing_rounded", "easting_m", "northing_m"]:
        if key in data:
            del data[key]
    return data


def lower_case_animal_type(data):
    """
    Lowercase animal type column to avoid duplicate categories. ie: Cat and cat
    """
    data["animal_group_parent"] = data["animal_group_parent"].str.lower()
    return data


def convert_to_datetime_format(data):
    """
    Convert the date_time_of_call as a pd.datetime type
    """
    data["date_time_of_call"] = pd.to_datetime(
        data["date_time_of_call"], format="%d/%m/%Y %H:%M"
    )
    return data


def remove_incoherent_values(data):
    """
    Remove incoherent values, seen for a low latitude compared to London's Latitude
    """
    return data[data["latitude"] > 30]


def remove_duplicate_values(data):
    """
    Remove duplicate values in the dataframe
    """
    data = data.drop_duplicates()
    return data


def remove_unused_columns(data):
    """
    Remove unused columns bases on the correlation table and data analyse
    """
    # Based on correlation table, we see that incident_number, uprn, usrn has low relation with other variables.
    # These parameters are indepentdent and no strong affected to data performance, so we can ignore it
    data = delete_feature(data, "incident_number")
    data = delete_feature(data, "type_of_incident")

    data = delete_feature(data, "cal_year")
    data = delete_feature(data, "fin_year")

    # UPRNs are the unique identifiers for every addressable location in Great Britain
    data = delete_feature(data, "uprn")

    # USRNs are the unique identifiers for every street in Great Britain
    data = delete_feature(data, "usrn")

    # remove related columns (with coor ~= 1)
    data = delete_feature(data, "hourly_notional_cost")
    data = delete_feature(data, "pump_hours_total")

    for column in [
        "postcode_district",
        "street",
        "stn_ground_name",
        "borough_code",
        "ward",
        "ward_code",
        "final_description",
    ]:
        data = delete_feature(data, column)
    return data


def add_columns_for_date(data):
    """
    Add columns to divide the date into multiple numerical and categorical columns
    """
    month_type = pd.CategoricalDtype(
        categories=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        ordered=True,
    )

    day_type = pd.CategoricalDtype(
        categories=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        ordered=True,
    )

    data["year"] = data["date_time_of_call"].dt.year
    data["month"] = data["date_time_of_call"].dt.month
    data["dayofweek"] = data["date_time_of_call"].dt.day_of_week

    data = data.replace({"month": month_dic})
    data = data.replace({"dayofweek": dayofweek_dic})
    data["hour"] = data["date_time_of_call"].dt.hour
    data["month"] = data["month"].astype(month_type)
    data["dayofweek"] = data["dayofweek"].astype(day_type)

    return data
