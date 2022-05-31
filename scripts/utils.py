# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      utils.py                                           ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: Branly, Tran Quoc <->                          ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://github.com/StephaneBranly              +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2022/05/31 18:39:07 by Branly, Tran Quoc   ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #


def numeric_categorical_attributs_split(data):
    """
    Returns the column names splitted by numerical and categorical columns
    """
    numerics = []
    objects = []
    for c in data.columns:
        if data.dtypes[c] == "object":
            objects.append(c)
        else:
            numerics.append(c)

    return objects, numerics


def pretty_pct_round(value):
    """
    Returns a pretty pourcentage round float
    """
    return round(value * 100, 1)


def delete_feature(data, features):
    """
    Remove features in the dataframe
    """
    if features in data.columns:
        del data[features]
    return data


month_dic = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

dayofweek_dic = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


class couleurs:
    ENTETE = "\033[95m"
    OKBLEU = "\033[94m"
    OKCYAN = "\033[96m"
    OKVERT = "\033[92m"
    ATTENTION = "\033[93m"
    KO = "\033[91m"
    FIN = "\033[0m"
    GRAS = "\033[1m"
    SOUSLIGNE = "\033[4m"


animal_index_color_palette = {
    "cat": 1,
    "bird": 0,
    "dog": 3,
    "fox": 4,
    "horse": 5,
    "unknown - domestic animal or pet": 7,
    "deer": 2,
    "unknown - wild animal": 8,
    "squirrel": 6,
}
