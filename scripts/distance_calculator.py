"""
This module uses haversine module to return the distance of two countries with configurable precision
"""

from haversine import haversine
from typing import Literal


class DistanceCalculator:
    def __init__(self, unit: Literal["km", "mi"] = "km", precision: int = 1) -> None:
        self.unit = unit
        self.precision = precision

    def calculate_distance(
        self, guessed_country: tuple[int, int], correct_country: tuple[int, int]
    ) -> float:
        return round(
            haversine(guessed_country, correct_country, unit=self.unit), self.precision
        )
