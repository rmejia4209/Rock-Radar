import os
from utils.utils import extract_data, save_json_data
from custom_types.custom_types import (
    RouteDict, RouteDetails, ReviewStatsDict, CSVData
)


def generate_area_list(area: str) -> list[str]:
    """
    Generates a list of areas from the given string.

    Args:
        area (str): "Crag > Subarea > Subarea > Main Area"

    Returns:
        list[str]: [Main Area, Subarea, ..., Subarea, Crag]
    """
    area_list = area.split(" > ")
    if len(area_list) and area_list[-1] == 'International':
        area_list = area_list[:-2]
    else:
        area_list.append('USA')
    area_list.reverse()
    return area_list


def organize_route_details(
    route_data: list[str],
    num_reviews: int,
    route_id: str
) -> RouteDetails:
    """
    Extracts the route's information from data and returns a RouteDetails
    dictionary.

    Args:
        route_data (list[str]): The route's data in a list format
        num_reviews (int): The number of reviews a route has received
        route_id: The route's id

    Returns:
        RouteDetails: a dictionary containing the info on a the given route
    """
    route_types = route_data[5].replace('TR', 'Top Rope')
    return {
        "name": route_data[0],
        "area": generate_area_list(route_data[1]),
        "grade": route_data[6],
        "route_types": route_types.split(", "),
        "num_pitches": route_data[7],
        "length": route_data[8],
        "rating": float(route_data[3]),
        "num_reviewers": num_reviews,
        "coordinates": (float(route_data[9]), float(route_data[10]))
    }


def build_route_dict(routes: CSVData) -> RouteDict:
    """
    Builds a RouteDict based on the data extracted from the csv file

    Args:
        routes (CSVData): route data from a csv file

    Returns:
        RouteDict: A dictionary with details on multiple routes
    """
    src = os.path.join(os.path.dirname(__file__), "reviews_data.json")
    num_reviews_by_id: ReviewStatsDict = extract_data(src)

    route_data: RouteDict = {}
    for route in routes:
        route_id = route[2].split("/")[-2]  # extract the id from the url
        num_reviews = num_reviews_by_id.get(route_id, 0)

        route_data[route_id] = organize_route_details(
            route,
            num_reviews,
            route_id
        )
    return route_data


def build_json_sources(areas: list[str] | None = None) -> None:
    """
    Builds a json file that stores a RouteDict.

    Args:
        areas (list[str]): Optional list of areas to build a source file for

    """
    areas = list(map(lambda area: area.replace(' ', '_').lower(), areas))
    src_folder = os.path.join(os.path.dirname(__file__), 'crags_by_area')
    dest_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'data', 'crags_by_area')

    for file in os.listdir(src_folder):
        file = file.split('.')[0]
        if areas and file not in areas:
            continue
        data = extract_data(os.path.join(src_folder, f'{file}.csv'))
        save_json_data(
            os.path.join(dest_folder, f'{file}.json'), build_route_dict(data)
        )
