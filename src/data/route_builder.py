from __future__ import annotations
import os
from utils.utils import extract_data
from custom_types.crag import Route, Area
from custom_types.custom_types import RouteDict


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
