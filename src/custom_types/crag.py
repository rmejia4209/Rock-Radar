from __future__ import annotations
# from functools import total_ordering
from custom_types.node import Node
from custom_types.grade import Grade


class RouteFilter:
    _lower_grade: Grade
    _upper_grade: Grade

    def __init__(self):
        self._lower_grade = Grade("5.0")
        self._upper_grade = Grade("5.15")

    def __str__(self):
        txt = "Current Filter\n"
        txt += f"\tMinimum Grade: {self._lower_grade}\n"
        txt += f"\tMaximum Grade: {self._upper_grade}\n"
        return txt

    @property
    def lower_grade(self) -> Grade:
        """Returns the lower grade bound"""
        return self._lower_grade

    @property
    def upper_grade(self) -> Grade:
        """Returns the upper grade bound"""
        return self._upper_grade

    @lower_grade.setter
    def lower_grade(self, grade: Grade | str) -> None:
        """Setter function for setting the lower grade bound"""
        self._lower_grade = grade if isinstance(grade, Grade) else Grade(grade)

    @upper_grade.setter
    def upper_grade(self, grade: Grade | str) -> None:
        """Setter function for setting the upper grade bound"""
        self._upper_grade = grade if isinstance(grade, Grade) else Grade(grade)

    def is_match(self, route: Route) -> bool:
        """TODO"""
        # Check 1: Is the route's grade within the min and max grades?
        in_grade_range = route.grade.is_in_range(
            self._lower_grade, self._upper_grade
        )
        return in_grade_range

    def more_deets(self, route: Route):
        print(f"Lower Limit Value: {self._lower_grade.value}")
        print(f"Upper Limit Value: {self._upper_grade.value}")
        print(f"Route's limit: {route.grade.value}")


class Area(Node):

    _name: str
    _parent: Area | None
    _children: list[Area] | list[Route]
    _coordinates: tuple[float, float]
    _children: list[Area] | list[Route]

    _route_filter: RouteFilter = RouteFilter()

    def __init__(self, name: str, parent: Area | None = None):
        super().__init__(name, parent=parent)

        self._coordinates = None
        self._total_routes = 0
        self._matching_routes = 0
        self._raw_score = 0
        self._log_normalize_score = 0
        self._popularity = 0

    def __str__(self):
        return f"{self._name} ({self._matching_routes})"

    @property
    def coordinates(self) -> tuple[float, float] | None:
        """Returns the areas coordinates"""
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates) -> None:
        """Sets the coordinates of the area"""
        if not self._coordinates:
            self._coordinates = coordinates

    @property
    def route_filter(self) -> RouteFilter:
        """Returns the class filter attribute"""
        return type(self)._route_filter

    @property
    def total_num_routes(self) -> int:
        return self._total_routes

    @property
    def num_matching_routes(self) -> int:
        return self._matching_routes

    def calculate_total_num_routes(self) -> int:
        """Calculates the total number of routes in an area"""
        # Base case - children are routes
        if self.is_leaf_parent:
            self._total_routes = len(self._children)

        # Recursive case - children are areas
        else:
            self._total_routes = 0
            for area in self._children:
                area.calculate_total_num_routes()
                self._total_routes += area.total_num_routes
        return

    def init_stats(self) -> None:
        self.calculate_total_num_routes()
        self.calculate_stats(self._route_filter)
        return

    def reset_stats(self) -> None:
        """Method to reset the stats"""
        self._matching_routes = 0
        self._raw_score = 0

    def get_stats(self) -> dict[str, int | float]:
        return {
            "matching_routes": self._matching_routes,
            "raw_score": self._raw_score
        }

    def calculate_stats(self) -> None:
        """Calculates the stats based on the class filter"""
        self.reset_stats()
        for child in self._children:
            if self.is_leaf_parent:
                child.calculate_stats(self.route_filter)
            else:
                child.calculate_stats()

            child_stats = child.get_stats()
            self._matching_routes += child_stats.get("matching_routes", 0)
            self._raw_score += child_stats.get("raw_score", 0)
        return

    def set_filter(self, lower_grade, upper_grade) -> None:
        self._route_filter.lower_grade = lower_grade
        self._route_filter.upper_grade = upper_grade
        # Recalculate stats here


class Route(Node):
    _id: str
    _name: str
    _url: str
    _grade: Grade
    _route_types: list[str]
    _num_pitches: int
    _length: int
    _rating: float
    _popularity: int
    _crag: Area | None
    _stats: dict[str, int | float]

    def __init__(
        self,
        mp_id: str, name: str, url: str, grade: str, route_types: list[str],
        num_pitches: int, length: int, rating: float, popularity: int
    ) -> None:
        super().__init__(f"{name} ({grade})", is_leaf=True)
        self._id = mp_id
        self._url = url
        self._grade = Grade(grade)
        self._route_types = route_types
        self._num_pitches = num_pitches
        self._length = length
        self._rating = rating
        self._popularity = popularity

    @property
    def crag(self) -> Area:
        """Returns the crag of the route"""
        return self._parent

    @crag.setter
    def crag(self, area: Area) -> None:
        """Sets the parent of the route"""
        self._parent = area

    @property
    def name(self) -> str:
        """Returns the name of the route"""
        return self._name

    @property
    def grade(self) -> Grade:
        """Returns the grade of the route"""
        return self._grade

    @property
    def rating(self) -> float:
        """Returns the rating of the route"""
        return round(self._rating, 2)

    def _set_stats(self, stats: dict[str, int | float]) -> None:
        """Sets the route's stats"""
        self._stats = stats

    def get_stats(self) -> dict[str, int | float]:
        """Returns the route's stats"""
        return self._stats

    def calculate_stats(
        self, route_filter: RouteFilter
    ) -> dict[str, int | float]:
        """
        Calculates the route's stats if it meets the filter requirements
        """
        if route_filter.is_match(self):
            self._set_stats({
                "matching_routes": 1,
                "raw_score": round(self._rating * self._popularity, 2)
            })
        else:
            self._set_stats({})
