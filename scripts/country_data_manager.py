import pandas as pd
import sqlite3


class DatabaseHandler:
    def __init__(
        self,
        db_path: str = "countries.db",
        positions_csv_path="static/countries.csv",
    ) -> None:
        self.db_path = db_path
        self.positions_csv_path = positions_csv_path
        self.initialize_database()

    def get_country_details(self, country_code: str) -> tuple[str, float, float, str]:
        query = (
            f"SELECT * FROM countries_position WHERE country_code = '{country_code}'"
        )
        return self.cursor.execute(query).fetchone()

    def initialize_database(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        positions_query = (
            "CREATE TABLE IF NOT EXISTS countries_position ("
            "country_code TEXT PRIMARY KEY, "
            "latitude REAL NOT NULL, "
            "longitude REAL NOT NULL, "
            "name TEXT NOT NULL)"
        )

        self.cursor.execute(positions_query)

        self.add_data_to_database()

    def add_data_to_database(self) -> None:
        countries_position_df = pd.read_csv(
            self.positions_csv_path, keep_default_na=False
        )
        countries_position_df.to_sql(
            "countries_position", self.conn, if_exists="replace", index=False
        )
