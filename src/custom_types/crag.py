from __future__ import annotations
from functools import total_ordering
from custom_types.node import Node


@total_ordering
class Grade:
    _grade: str
    _base: int
    _suffix: str
    _value: float

    # Grade ranking class attributes
    _loose_grade_equivalency: dict[str, list[str]] = {
        "a": ["a", "-", "a/b"],
        "b": ["a/b", "b", "", "b/c"],
        "c": ["b/c", "c", "+", "c/d"],
        "d": ["+", "c/d", "d"],
        "": ["-", "", "+"]  # Need to verify this edge case
        }

    _strict_grade_ranking: list[str] = []
    for grade_list in _loose_grade_equivalency.values():
        _strict_grade_ranking.extend([grade for grade in grade_list])

    def __init__(self, grade):
        self._grade = grade
        self._base, self._suffix = self._get_base_and_suffix()
        self._value = self._determine_value()

    def __str__(self) -> str:
        """
        Returns the grade string representation. (i.e., 5.10b/c, 5.9+, etc)
        """
        return self._grade

    def __eq__(self, other: Grade) -> bool:
        """Returns true if the two grades are equivalent"""
        return self._value == other.value

    def __lt__(self, other: Grade) -> bool:
        """Returns true if self has a value less than other"""
        return self._value < other.value

    @property
    def value(self) -> float:
        """Returns the grade's numerical score. Useful for sorting grades"""
        return self._value

    @property
    def base(self) -> int:
        """Returns a grade's base grade (i.e., 5.10a -> 10)"""
        return self._base

    @property
    def suffix(self) -> str:
        """Returns a grade's suffix (i.e., 5.10b/c -> b/c)"""
        return self._suffix

    @staticmethod
    def get_all_common_grades() -> list[Grade]:
        """Returns a list of all common grades"""
        grade_strings = [
            "5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8",
            "5.9", "5.10a", "5.10b", "5.10c", "5.10d", "5.11a", "5.11b",
            "5.11c", "5.11d", "5.12a", "5.12b", "5.12c", "5.12d", "5.13a",
            "5.13b", "5.13c", "5.13d", "5.14a", "5.14b", "5.14c", "5.14d",
            "5.15a", "5.15b", "5.15c", "5.15d"
        ]
        return sorted([Grade(grade) for grade in grade_strings])

    def _get_base_and_suffix(self) -> tuple[int, str]:
        """
        Returns a tuple with the base grade (1 - 14) and the grade's suffix
        (a, b, c, a/b, +, etc.)
        """
        # Remove the 5. prefix
        main_component = self._grade.split(".")[1]
        main_component = main_component.split(" ", 1)[0]
        base = ""
        suffix = ""
        for char in main_component:
            if char.isdigit():
                base += char
            else:
                suffix += char

        return int(base), suffix

    def _determine_value(self) -> float:
        """Returns a float used to compare grades with one another"""
        for value, suffix in enumerate(self._strict_grade_ranking, start=10):
            if self._suffix == suffix:
                return round(self._base + (value/100), 2)

    def _loose_ge(self, min_bound: Grade) -> bool:
        """
        Returns true if grade's suffix is loosely equivalent
        to the given minimum (i.e., 5.10+ == 5.10d).
        """
        if (
            min_bound.base == self._base
            and self._suffix in self._loose_grade_equivalency[min_bound.suffix]
        ):
            return True
        return False

    def _loose_le(self, max_bound: Grade) -> bool:
        """
        Returns true if grade's suffix is loosely equivalent
        to the given maximum (i.e., 5.10b/c == 5.10b).
        """
        if (
            max_bound.base == self._base
            and self._suffix in self._loose_grade_equivalency[max_bound.suffix]
        ):
            return True
        return False

    def is_in_range(self, min_bound: Grade, max_bound: Grade) -> bool:
        """
        Returns true if the grade is greater than or equal to the min bound
        and less than or equal to the max bound. Returns false otherwise.
        """
        # TODO: test edge cases
        # TODO: bug here - 13b fails 13d filter
        if min_bound <= self <= max_bound:
            return True
        elif self._loose_ge(min_bound) or self._loose_le(max_bound):
            return True
        return False


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
    _coordinates: tuple[float, float]
    _children: list[Area] | list[Route]

    _route_filter: RouteFilter = RouteFilter()

    def __init__(self, name: str, parent: Area | None = None):
        super().__init__(name, parent=parent)

        self._coordinates = None
        self._children = []

        self._total_routes = 0
        self._matching_routes = 0
        self._raw_score = 0
        self._log_normalize_score = 0
        self._popularity = 0

    @property
    def coordinates(self) -> tuple[float, float] | None:
        return self._coordinates

    @property
    def route_filter(self) -> RouteFilter:
        return self._route_filter

    @property
    def total_num_routes(self) -> int:
        return self._total_routes

    @property
    def num_matching_routes(self) -> int:
        return self._matching_routes

    @coordinates.setter
    def coordinates(self, coordinates) -> None:
        if not self._coordinates:
            self._coordinates = coordinates

    def _add_child(self, child: Area | Route) -> None:
        # TODO: Refactor
        """Adds a child to children"""
        if (
            len(self._children) == 0
            or isinstance(child, type(self._children[0]))
        ):
            self._children.append(child)
        else:
            raise Exception("An area can't contain both subareas and routes!")

    def calculate_total_num_routes(self) -> int:
        """
        Calculates the total number of routes in an area.
        """
        # Base case - children are routes
        if self.is_leaf_parent:
            self._total_routes = len(self._children)
            return self._total_routes

        # Recursive case - children are areas
        self._total_routes = 0
        for area in self._children:
            self._total_routes += area.calculate_total_num_routes()
        return self._total_routes

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

    def calculate_stats(
        self, route_filter: RouteFilter | None = None
    ) -> dict[str, int | float]:
        if route_filter is None:
            route_filter = self._route_filter
        self.reset_stats()
        for child in self._children:
            child_stats = child.calculate_stats(route_filter)
            self._matching_routes += child_stats.get("matching_routes", 0)
            self._raw_score += child_stats.get("raw_score", 0)

        return self.get_stats()

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
        return self._parent

    @crag.setter
    def crag(self, area: Area) -> None:
        self._parent = area

    @property
    def name(self) -> str:
        return self._name

    @property
    def grade(self) -> Grade:
        return self._grade

    @property
    def rating(self) -> float:
        return round(self._rating, 2)

    def calculate_stats(
        self, route_filter: RouteFilter
    ) -> dict[str, int | float]:
        """
        TODO:
        """
        if not route_filter.is_match(self):
            return {}
        return {
            "matching_routes": 1,
            "raw_score": round(self._rating * self._popularity, 2)
        }
