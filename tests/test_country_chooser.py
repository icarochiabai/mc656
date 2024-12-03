from scripts.country_chooser import CountryChooser
from datetime import datetime
from zoneinfo import ZoneInfo
from freezegun import freeze_time
import os

CSV_PATH = "static/countries_position.csv"


# Test the initialization of CountryChooser
def test_init_with_seed_and_timezone():
    seed = 1234
    chooser = CountryChooser(path=CSV_PATH, seed=seed, timezone="America/New_York")
    assert chooser.seed == seed
    assert chooser.timezone == ZoneInfo("America/New_York")

    # Since we didn't run the choose function yet, no parameters should be set yet
    assert chooser.today_country_id is None
    assert chooser.yesterday_country_id is None

    # Running the choose function and asserting that the result is Sweden
    with freeze_time("2024-11-13 18:00:00"):
        result = chooser.choose()
        assert result == {
            "country": "SE",
            "latitude": 60.128161,
            "longitude": 18.643501,
            "name": "Sweden",
        }
        assert chooser.today_country_id == 193
        assert chooser.yesterday_country_id != chooser.today_country_id

    # Testing after one day and checking if the country changes and yesterday's ID was updated
    with freeze_time("2024-11-14 18:00:00"):
        new_result = chooser.choose()
        assert new_result == {
            "country": "MG",
            "latitude": -18.766947,
            "longitude": 46.869107,
            "name": "Madagascar",
        }
        assert chooser.today_country_id == 138
        assert chooser.yesterday_country_id == 193


def test_init_without_seed(mocker):
    # Mocking urandom call to always return the same random bytes so the seed will be the same
    mocker.patch.object(os, "urandom", return_value=b"\x87S\xdb'\x1caX\x0b")
    chooser = CountryChooser(path=CSV_PATH)
    assert chooser.seed == 9751378579213604875


def test_init_without_timezone():
    # Since no timezone was provided, it should use default value, i.e UTC
    chooser = CountryChooser(path=CSV_PATH)
    assert chooser.timezone == ZoneInfo("Etc/UTC")


def test_hash_seed():
    # Asserting the correct hash is being produced for November 15th 2024 and seed 31415926
    seed = 31415926
    chooser = CountryChooser(path=CSV_PATH, seed=seed)
    date = datetime(2024, 11, 15)
    result = chooser.get_hashed_seed(date)
    assert result == "567e85a9f70a72c6bb2b8f96b237b9dae1a1a85f66a509b06a1ccf7b0da597d7"
