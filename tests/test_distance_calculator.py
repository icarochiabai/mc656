import pytest
from scripts.distance_calculator import DistanceCalculator

# Coordinates from IC - Instituto de Computação and RU - Restaurante Universitário
ic_coordinates = (-22.8135277, -47.0640489)
ru_coordinates = (-22.8175139, -47.0747712)

# Distance between both
distance_between_both_km = 1.1850012302276625
distance_between_both_mi = 0.736325626948029



def test_distance_default_precision():
    # The actual distance is around 1.18km, so it will round to 1.2 km or 0.7 miles.
    # Since we're not specifying precision, it will use one decimal place
    assert (
        DistanceCalculator().calculate_distance(ic_coordinates, ru_coordinates) == round(distance_between_both_km, 1)
    )
    assert (
        DistanceCalculator(unit="km").calculate_distance(ic_coordinates, ru_coordinates)
        == round(distance_between_both_km, 1)
    )
    assert (
        DistanceCalculator(unit="mi").calculate_distance(ic_coordinates, ru_coordinates)
        == round(distance_between_both_mi, 1)
    )

    # Asserting distance works independently of direction
    assert DistanceCalculator().calculate_distance(
        ic_coordinates, ru_coordinates
    ) == DistanceCalculator().calculate_distance(ru_coordinates, ic_coordinates)


@pytest.mark.parametrize("precision", list(range(1, 15)))
def test_distance_custom_precision(precision):
    distance_calculator_km = DistanceCalculator(unit="km", precision=precision)
    distance_calculator_mi = DistanceCalculator(unit="mi", precision=precision)

    assert distance_calculator_km.calculate_distance(ic_coordinates, ru_coordinates) == round(distance_between_both_km, precision)
    assert distance_calculator_mi.calculate_distance(ic_coordinates, ru_coordinates) == round(distance_between_both_mi, precision)
