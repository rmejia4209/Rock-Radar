from __future__ import annotations
from functools import total_ordering


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

