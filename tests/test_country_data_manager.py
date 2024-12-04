import os
import pytest
import sqlite3
from tempfile import NamedTemporaryFile

from scripts.country_data_manager import DatabaseHandler


@pytest.fixture
def temp_csv_path():
    """
    Creates a temporary CSV file for testing
    """

    with NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_csv:
        temp_csv.write("country_code,latitude,longitude,name\n")
        temp_csv.write("XE,83.9824,-41.3111,Xen\n")
        temp_csv.write("RH,-129.6069,-80.9338,Ravelholm\n")
    yield temp_csv.name

    # Clean up the temporary CSV file after the test
    if os.path.exists(temp_csv.name):
        os.remove(temp_csv.name)


@pytest.fixture
def db_handler(temp_csv_path):
    """
    Creates database handler to be used for testing
    """
    yield DatabaseHandler(db_path=":memory:", positions_csv_path=temp_csv_path)


def test_database_initialization(db_handler):
    """
    Test database initialization and table creation
    """

    # Verify database connection
    assert hasattr(db_handler, "conn")
    assert hasattr(db_handler, "cursor")

    # Check if table exists
    db_handler.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = db_handler.cursor.fetchall()
    assert any("countries_position" in table for table in tables)


def test_get_country_details(db_handler):
    """
    Test retrieving country details from the database
    """

    # Test retrieving existing country
    us_details = db_handler.get_country_details("XE")
    assert us_details is not None
    assert us_details[0] == "XE"  # country code
    assert us_details[1] == 83.9824  # latitude
    assert us_details[2] == -41.3111  # longitude
    assert us_details[3] == "Xen"  # name


def test_get_country_details_nonexistent(db_handler):
    """
    Test retrieving details for a non-existent country
    """

    # Test retrieving non-existent country
    nonexistent_details = db_handler.get_country_details("ZZ")
    assert nonexistent_details is None


def test_if_data_was_added_to_database(db_handler):
    """
    Test adding data to the database from CSV
    """

    # Verify data was added correctly
    db_handler.cursor.execute("SELECT COUNT(*) FROM countries_position")
    count = db_handler.cursor.fetchone()[0]
    assert count > 0  # Ensure data was added


def test_database_connection_closure(db_handler):
    """
    Test that database connection can be properly closed
    """

    # Close the connection
    db_handler.conn.close()

    # Verify connection is closed
    with pytest.raises(sqlite3.ProgrammingError):
        db_handler.cursor.execute("SELECT 1")
