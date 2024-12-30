from __future__ import annotations
from custom_types.node import Node
from custom_types.grade import Grade
from custom_types.ranking_model import RankingModel

# TODO code smells
# Normalize data to eliminate TR and Top Rope
# Area/Route stat passing (i.e., route types & grades)


class RouteFilterWidget:
    """.DS_Store"""

    _lower_grade: Grade
    _upper_grade: Grade
    _min_len: int
    _min_num_pitches: int
    _route_types = {'Trad': 'Trad', 'Sport': 'Sport', 'Top Rope': 'TR'}

    def __init__(self):
        self._lower_grade = Grade("5.0")
        self._upper_grade = Grade("5.15")
        self._min_len = 0
        self._min_num_pitches = 0
        self._selected_route_types = list(type(self)._route_types.values())

    @property
    def available_route_types(self) -> list[str]:
        """Returns the available route types"""
        return list(type(self)._route_types.keys())

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

    def set_min_num_pitches(self, val: int) -> None:
        """Sets the minimum number of pitches for the filter"""
        self._min_num_pitches = val

    def set_min_length(self, val: int) -> None:
        """Sets the minimum number of pitches for the filter"""
        self._min_len = val

    def set_route_types(self, route_types: list[str]) -> None:
        """Sets the selected route types based on the provided argument"""
        self._selected_route_types.clear()
        self._selected_route_types = [
            type(self)._route_types[val] for val in route_types
        ]

    def is_match(self, route: Route) -> bool:
        """
        Returns true if the route is a match based on the currently set
        criteria
        """
        if route.num_pitches < self._min_num_pitches:
            return False

        if route.length < self._min_len:
            return False

        if not route.grade.is_in_range(self._lower_grade, self._upper_grade):
            return False

        return any(
            rt in self._selected_route_types for rt in route.route_types
        )


class Area(Node):

    _name: str
    _parent: Area | None
    _children: list[Area] | list[Route]
    _coordinates: tuple[float, float]
    _children: list[Area] | list[Route]
    _total_routes: int
    _matching_routes: int
    _popularity: int
    _rating: float
    _score: float
    _avg_popularity: float
    _avg_rating: float
    _avg_score: float
    _route_types: dict[str, int]

    _route_filter: RouteFilterWidget = RouteFilterWidget()
    _ranking_model: RankingModel = RankingModel()
    _node_attributes: dict[str, str] = {
        "name": "_name",
        "matches": "_matching_routes",
        "total number of routes": "_total_routes",
        "popularity": "_popularity",
        "rating": "_rating",
        "score": "_score",
        "average popularity": "_avg_popularity",
        "average rating": "_avg_rating",
        "average score": "_avg_score"
    }
    _leaf_attributes: dict[str, str] = {
        "name": "_name",
        "grade": "_grade",
        "popularity": "_popularity",
        "rating": "_rating",
        "score": "_score",
        "number of pitches": "_num_pitches",
        "length": "_length"
    }
    _metric: str = "_matching_routes"

    def __init__(self, name: str, parent: Area | None = None):
        super().__init__(name, parent=parent)

        self._coordinates = None
        self._total_routes = 0
        self._matching_routes = 0
        self._popularity = 0
        self._rating = 0
        self._score = 0
        self._avg_popularity = 0
        self._avg_rating = 0
        self._avg_score = 0
        route_types = Area._route_filter.available_route_types
        self._route_types = {route_type: 0 for route_type in route_types}

    def __str__(self):
        metric = getattr(self, Area._metric)
        if isinstance(metric, float):
            metric = f" ({(round(metric, 1))})"
        else:
            metric = f" ({metric})"
        return f"{self._name}{metric}"

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
    def route_filter(self) -> RouteFilterWidget:
        """Returns the class filter attribute"""
        return type(self)._route_filter

    @property
    def total_num_routes(self) -> int:
        return self._total_routes

    @property
    def num_matching_routes(self) -> int:
        return self._matching_routes

    @property
    def route_types(self) -> dict[str, int]:
        return self._route_types

    @property
    def models(self) -> list[str]:
        """Returns the available ranking model options"""
        return type(self)._ranking_model.get_options()

    @property
    def logistic_coefficient_limits(self) -> tuple[int, int]:
        return type(self)._ranking_model.get_logistic_coefficient_limits()

    def get_area_metrics(self) -> list[str]:
        """
        Returns the available statistics that may be displayed when printed
        """
        metrics = [stat.title() for stat in type(self)._node_attributes.keys()]
        for metric in ['Name', 'Popularity', 'Score', "Rating"]:
            metrics.remove(metric)
        return metrics

    def set_area_metric(self, metric: str) -> None:
        """Sets the metric that is displayed"""
        type(self)._metric = type(self)._node_attributes.get(metric.lower())

    def get_crag_metrics(self) -> list[str]:
        """
        Returns the available statistics that may be displayed when printed
        """
        metrics = [stat.title() for stat in type(self)._leaf_attributes.keys()]
        for metric in ['Name', 'Grade', 'Score', "Rating"]:
            metrics.remove(metric)
        return metrics

    def set_crag_metric(self, metric: str) -> None:
        """Sets the metric that is displayed"""
        Route._metric = type(self)._leaf_attributes.get(metric.lower())

    def set_filter(self, lower_grade, upper_grade) -> None:
        self._route_filter.lower_grade = lower_grade
        self._route_filter.upper_grade = upper_grade
        # Recalculate stats here

    def set_ranking_model(self, model: str) -> None:
        """Sets the ranking model"""
        type(self)._ranking_model.set_model(model)
        return

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
        self.calculate_stats()
        return

    def reset_stats(self) -> None:
        """Method to reset the stats"""
        self._matching_routes = 0
        self._popularity = 0
        self._rating = 0
        self._score = 0

    def get_stats(self) -> dict[str, int | float]:
        return {
            "matching_routes": self._matching_routes,
            "popularity": self._popularity,
            "rating": self._rating,
            "score": self._score,
            'Trad': self._route_types['Trad'],
            'Sport': self._route_types['Sport'],
            'Top Rope': self._route_types['Top Rope']
        }

    def increment_stats(self, child_stats: dict[str, int]) -> None:
        """Increments stats based on the children's stats"""
        self._matching_routes += child_stats.get("matching_routes", 0)
        self._popularity += child_stats.get("popularity", 0)
        self._rating += child_stats.get("rating", 0)
        self._score += child_stats.get("score", 0)
        self._route_types['Trad'] += child_stats.get("Trad", 0)
        self._route_types['Sport'] += child_stats.get("Sport", 0)
        self._route_types['Top Rope'] += child_stats.get("Top Rope", 0)

    def calculate_averages(self) -> None:
        """Calculates the averaged stats"""
        avgs = ["_avg_popularity", "_avg_rating", "_avg_score"]
        stats = ["_popularity", "_rating", "_score"]
        for avg, stat in zip(avgs, stats):
            if self._matching_routes == 0:
                setattr(self, avg, 0)
            else:
                val = round((getattr(self, stat) / self._matching_routes), 1)
                setattr(self, avg, val)
        self._avg_popularity = int(self._avg_popularity)
        return

    def calculate_stats(self) -> None:
        """Calculates the stats based on the class filter"""
        self.reset_stats()
        for child in self._children:
            if self.is_leaf_parent:
                child.calculate_stats(
                    type(self)._route_filter, type(self)._ranking_model
                )
            else:
                child.calculate_stats()
            self.increment_stats(child.get_stats())
        self.calculate_averages()
        return


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
    _metric: str = "_rating"

    def __init__(
        self,
        mp_id: str, name: str, url: str, grade: str, route_types: list[str],
        num_pitches: int, length: int, rating: float, popularity: int
    ) -> None:
        super().__init__(name, is_leaf=True)
        self._id = mp_id
        self._url = url
        self._grade = Grade(grade)
        self._route_types = route_types
        self._num_pitches = num_pitches
        self._length = length
        self._rating = rating
        self._popularity = popularity
        self._score = 0

    def __str__(self):
        metric = getattr(self, Route._metric)
        if isinstance(metric, float):
            metric = f" ({round(metric, 1)})"
        else:
            # Do not display length metric if it is 1
            metric = f" ({metric})" if metric > 1 else ""

        return f"{self._name} {self._grade}{metric}"

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

    @property
    def length(self) -> int:
        """Returns the length of the route"""
        return self._length

    @property
    def num_pitches(self) -> int:
        """Returns the routes number of pitches"""
        return self._num_pitches

    @property
    def route_types(self) -> list[str]:
        """Returns the route's types"""
        return self._route_types

    def _set_stats(self, stats: dict[str, int | float]) -> None:
        """Sets the route's stats"""
        self._stats = stats

    def get_stats(self) -> dict[str, int | float]:
        """Returns the route's stats"""
        return self._stats

    def calculate_stats(
        self, route_filter: RouteFilterWidget, ranking_model: RankingModel
    ) -> dict[str, int | float]:
        """
        Calculates the route's stats if it meets the filter requirements
        """
        if route_filter.is_match(self):
            self._score = ranking_model.get_score(
                self._popularity, self._rating
            )
            self._set_stats({
                'matching_routes': 1,
                'popularity': self._popularity,
                'rating': self._rating,
                'score': self._score,
                'Trad': 1 if 'Trad' in self._route_types else 0,
                'Sport': 1 if 'Sport' in self._route_types else 0,
                'Top Rope': 1 if 'TR' in self._route_types else 0
            })
        else:
            self._set_stats({
                'Trad': 1 if 'Trad' in self._route_types else 0,
                'Sport': 1 if 'Sport' in self._route_types else 0,
                'Top Rope': 1 if 'TR' in self._route_types else 0
            })
