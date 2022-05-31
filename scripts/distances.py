# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      distances.py                                       ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: Branly, Tran Quoc <->                          ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://github.com/StephaneBranly              +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2022/05/31 18:39:02 by Branly, Tran Quoc   ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import nearest_points
import matplotlib.pyplot as plt
import haversine as hs
import math
import time
import pandas as pd

from .utils import *


def add_target(targets, column_name, featureType, selector, display_color="red"):
    """
    Add a target in the targets
    """
    new_target = {
        "column_name": column_name,
        "featureType": featureType,
        "selector": selector,
        "display_color": display_color,
    }

    targets[column_name] = new_target
    return targets


def load_OSM_data(targets, areaId=None, bbox=None):
    """
    Load the OSM data for all the targets
    """
    overpass = Overpass()

    if areaId:
        for key in targets:
            target = targets[key]
            query = overpassQueryBuilder(
                area=areaId,
                elementType=target["featureType"],
                selector=target["selector"],
                includeGeometry=True,
            )
            targets[key]["features"] = overpass.query(query)
    elif bbox:
        for key in targets:
            target = targets[key]
            query = overpassQueryBuilder(
                bbox=bbox,
                featureType=target["featureType"],
                selector=target["selector"],
                includeGeometry=True,
            )
            targets[key]["features"] = overpass.query(query)
    else:
        raise Exception("You must provide an area to load the OpenStreetMap data")

    return targets


def print_number_of_features(targets):
    """
    Print the number of loaded OSM features for the targets
    """
    for key in targets:
        target = targets[key]
        print(f"{key} {couleurs.KO}#{len(target['features'].elements())}{couleurs.FIN}")


def get_nearest_point_of_polygon(
    poly_shape, loc, is_polygon, show_graph=False, fillColor="#DD0000"
):
    """
    Get the nearest point of the polygon from another point
    """
    if is_polygon:
        poly = Polygon([(a, b) for [a, b] in poly_shape])
    else:
        poly = LineString([(a, b) for [a, b] in poly_shape])
    point = Point(loc[1], loc[0])
    p1, _ = nearest_points(poly, point)

    tmp = list(zip(*p1.coords.xy))[0]

    if show_graph:
        plt.plot(*poly.exterior.xy, color="blue", label="Polygon")
        if is_polygon:
            plt.fill(*poly.exterior.xy, color=fillColor + "BB")
        plt.plot(
            [tmp[0], loc[1]],
            [tmp[1], loc[0]],
            color="#333",
            linestyle=":",
            label="Distance",
        )
        plt.scatter(*p1.coords.xy, color="red", label="Nearest point from polygon")
        plt.scatter(x=loc[1], y=loc[0], color="green", label="Location reference")
        plt.legend(loc="upper right")
        plt.show()
    return (tmp[1], tmp[0])


def get_nearest_feature_distance(
    features, point, show_graph=False, fillColor="#DD0000", feature_name=None
):
    """
    Get the distance of the nearest feature between an array of features and a point
    """
    minimal_distance = math.inf
    nearest_feature = None

    for feature in features:
        try:
            feature_type = feature.geometry().type
            if feature_type == "MultiPolygon":
                local_min = math.inf
                for poly_shape in feature.geometry().coordinates[0]:
                    nearest_point = get_nearest_point_of_polygon(
                        poly_shape, point, True
                    )
                    distance = hs.haversine(point, nearest_point, unit=hs.Unit.METERS)
                    if distance < local_min:
                        local_min = distance
                distance = local_min
            if feature_type in ["Polygon", "Polyline"]:
                nearest_point = get_nearest_point_of_polygon(
                    feature.geometry().coordinates[0], point, feature_type == "Polygon"
                )
                distance = hs.haversine(point, nearest_point, unit=hs.Unit.METERS)
            elif feature_type == "Point":
                distance = hs.haversine(
                    point,
                    (
                        feature.geometry().coordinates[1],
                        feature.geometry().coordinates[0],
                    ),
                    unit=hs.Unit.METERS,
                )
            if distance < minimal_distance:
                minimal_distance = distance
                nearest_feature = feature
        except:
            pass

    if show_graph:
        for feature in features:
            try:
                color = "red" if feature == nearest_feature else fillColor
                name = feature_name if feature_name else "feature"
                label = f"Nearest {name}" if feature == nearest_feature else f"{name}"
                feature_type = feature.geometry().type
                if feature_type == "MultiPolygon":
                    for poly_shape in feature.geometry().coordinates[0]:
                        poly = Polygon([(a, b) for [a, b] in poly_shape])
                        plt.plot(*poly.exterior.xy, color=color)
                        plt.fill(*poly.exterior.xy, color=fillColor + "BB", label=label)
                elif feature_type in ["Polygon", "Polyline"]:
                    poly = Polygon(
                        [(a, b) for [a, b] in feature.geometry().coordinates[0]]
                    )
                    plt.plot(*poly.exterior.xy, color=color, label=label)
                    if feature_type == "Polygon":
                        plt.fill(*poly.exterior.xy, color=fillColor + "BB")
                elif feature_type == "Point":
                    plt.scatter(
                        *feature.geometry().coordinates, color=color, label=label
                    )
            except:
                pass
        plt.scatter(x=point[1], y=point[0], color="blue", label="Location reference")
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc="upper right")
        plt.show()
    return minimal_distance


def plot_features(features, fillColor="#FF0000", key=None):
    """
    Display the features
    """
    for feature in features:
        try:
            feature_type = feature.geometry().type
            if feature_type == "MultiPolygon":
                for poly_shape in feature.geometry().coordinates[0]:
                    poly = Polygon([(a, b) for [a, b] in poly_shape])
                    plt.fill(*poly.exterior.xy, color=fillColor + "BB", label=key)
            elif feature_type in ["Polygon", "Polyline"]:
                poly = Polygon([(a, b) for [a, b] in feature.geometry().coordinates[0]])
                plt.plot(*poly.exterior.xy, color=fillColor + "BB", label=key)
                if feature_type == "Polygon":
                    plt.fill(*poly.exterior.xy, color=fillColor + "BB")
            elif feature_type == "Point":
                plt.scatter(*feature.geometry().coordinates, color=fillColor, label=key)
        except:
            pass


def plot_targets(targets):
    """
    Plot all the targets. Plot all fatures for each target
    """
    for k in targets:
        target = targets[k]
        plot_features(target["features"].elements(), target["display_color"], k)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(
        by_label.values(), by_label.keys(), loc="center left", bbox_to_anchor=(1, 0.5)
    )
    plt.show()


def calculate_distances(data, targets, save_path="computed_distances/"):
    """
    Calculate the nearest element distances for all points in a dataframe
    """
    for key in targets:
        print(
            f"{key} {couleurs.KO}#{len(targets[key]['features'].elements())}{couleurs.FIN}"
        )
        obj = targets[key]["features"].elements()
        start_time = time.time()
        column_name = f"nearest_{key}"
        distances_data = pd.DataFrame(
            {
                column_name: data[["latitude", "longitude"]].apply(
                    lambda x: get_nearest_feature_distance(
                        obj, (x.latitude, x.longitude)
                    ),
                    axis=1,
                )
            }
        )
        distances_data.to_csv(f"{save_path}/{key}_data.csv")
        print(
            f"--> {key} took {couleurs.OKVERT} {(time.time() - start_time)} seconds{couleurs.FIN}"
        )
