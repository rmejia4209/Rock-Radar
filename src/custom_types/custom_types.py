from typing import TypedDict


class RouteDetails(TypedDict):
    """
    Represents the details of a climbing route

    Attributes:
    -----------
    name: str
        The name of the route.
    area: list[str]
        A list of areas that specify the location of the route.
    url: str
        The route's mountain project url.
    grade: str
        The difficulty of the route.
    num_pitches: int
        The number of pitches for the route.
    length: int
        The total length of the route in feet.
    rating:
        The average rating given by climbers.
    num_reviewers: int
        The number of climbers that have reviewed the route.
    coordinates: tuple[float, float]
        The coordinates of the route's immediate parent area.
    """
    name: str
    area: list[str]
    url: str
    grade: str
    route_type: list[str]
    num_pitches: int
    length: int
    rating: float
    num_reviewers: int
    coordinates: tuple[float, float]


# Alias for data from a csv file
CSVData = list[list[str]]

# Alias for a dictionary that maps route id's to route details
RouteDict = dict[str, RouteDetails]

# Alias for a dictionary that maps route id's to number of reviews
ReviewStatsDict = dict[str, int]
