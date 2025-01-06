from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import os
import threading
from custom_types.crag import Route, Area
from custom_types.custom_types import RouteDict
from utils.utils import extract_data


def get_areas_available_for_download():
    """Returns all of the areas that have not been downloaded"""
    src = os.path.join(os.path.dirname(__file__), 'crags_by_area')
    saved_areas = list(
        map(
            lambda region: region.split('.')[0].replace('_', ' ').title(),
            os.listdir(src)
        )
    )
    areas = extract_data(os.path.join(os.path.dirname(src), 'area_map.json'))
    for area in saved_areas:
        areas.pop(area, None)
    return areas


def find_existing_area(root: Area, area_name: str) -> Area | None:
    """
    Iterates through the root's subareas and returns a match if found.

    Args:
        root (Area): The Area node being searched in
        area_name (str): The area being searched for

    Returns:
        Area | None: if a match is found, the area is returned otherwise none
    """
    for subarea in root.children:
        if subarea.name == area_name:
            return subarea
    return


def find_or_create_subarea(root: Area, area_name: str) -> Area:
    """
    Returns an existing subarea that matches the area's name or a newly
    created subarea.

    Args:
        root (Area): The Area node being searched in
        area_name (str): The area being searched for

    Returns:
        Area: an Area node with the given name
    """
    subarea = find_existing_area(root, area_name)
    subarea = Area(area_name, root) if subarea is None else subarea
    return subarea


def add_route_and_update_crag(crag: Area, route: Route) -> None:
    """
    Adds the route to the given crag and update's the route's crag.

    Args:
        crag (Area): The crag of the route
        route (Route): The route that is added to the crag
    """
    crag.add_child(route)
    route.crag = crag


def add_path(root: Area, path: list[str], route: Route) -> None:
    """
    Recursive function that creates a path from the given root.

    Args:
        root (Area): The root of the path
        path (list[str]): a list in the form of [Main Area, Subarea, ..., Crag]
        route
    """
    subarea = find_or_create_subarea(root, path[0])
    if len(path) > 1:
        add_path(subarea, path[1:], route)
    else:
        add_route_and_update_crag(subarea, route)


def build_area_tree() -> Area:
    """
    Builds an Area tree from the source files.

    Returns:
        Area: the root node of the area tree
    """
    src = os.path.join(os.path.dirname(__file__), 'crags_by_area')
    root = Area('Rock Radar')

    for file in os.listdir(src):
        data: RouteDict = extract_data(os.path.join(src, file))
        for route_id, route in data.items():
            length = int(route["length"]) if route["length"] else 0
            new_route = Route(
                route_id, route["name"], route["grade"],
                route["route_types"], int(route["num_pitches"]),
                length, float(route["rating"]), int(route["num_reviewers"])
            )
            add_path(root, route['area'], new_route)
    return root


def build_subtree(fp: str) -> Area:
    """
    Builds an Area tree from the given source file path.

    Args:
        fp (str): file path of source data

    Returns:
        Area: the root node of the area tree
    """

    root = Area('')
    data: RouteDict = extract_data(fp)
    for route_id, route in data.items():
        length = int(route["length"]) if route["length"] else 0
        new_route = Route(
            route_id, route["name"], route["grade"],
            route["route_types"], int(route["num_pitches"]),
            length, float(route["rating"]), int(route["num_reviewers"])
        )
        add_path(root, route['area'], new_route)
    return root.children[0]


def add_subtree_to_list(
    countries: list[Area], region_fp: str, usa: Area, lock: threading.Lock
) -> None:
    """
    Safely adds the regions subtree to the countries list or as a child
    of the USA node.

    Args:
        countries (list[Area]): list of countries trees
        region_fp (str): file path of region's source data
        usa (Area): USA node to add states
        lock (threading.Lock): thread lock to safely access the list/node
    """
    region = build_subtree(region_fp)

    with lock:
        if region.name == 'USA':
            state = region.children[0]
            state.parent = usa
            usa.add_child(state)
        else:
            countries.append(region)
    return


def build_area_tree_threaded() -> Area:
    """
    Builds an Area tree from the source files. Uses threads to speed the
    process up. Not recommend for less than TODO number of regions.

    Returns:
        Area: the root node of the area tree
    """

    root = Area('Rock Radar')
    usa = Area('')
    countries: list[Area] = []
    lock = threading.Lock()
    src_files = []
    src = os.path.join(os.path.dirname(__file__), 'crags_by_area')
    for file in os.listdir(src):
        src_files.append(os.path.join(src, file))

    with ThreadPoolExecutor(max_workers=4) as executor:
        for fp in src_files:
            executor.submit(
                add_subtree_to_list, countries, fp, usa, lock
            )

    countries.append(usa)
    for country in countries:
        root.add_child(country)
        country.parent = root

    return root
