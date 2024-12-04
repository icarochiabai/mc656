import pandas as pd
import sqlite3


class DatabaseHandler:
    def __init__(
        self,
        db_path: str = "countries.db",
        csv_path="static/countries.csv",
    ) -> None:
        self.db_path = db_path
        self.csv_path = csv_path
        self.initialize_database()

    def get_country_details(
        self, *, country_code: str = None, index: int = None
    ) -> tuple[int, str, float, float, str, float, int]:
        if country_code is None and index is None:
            raise RuntimeError("No parameters provided")

        if country_code is not None and index is not None:
            raise RuntimeError("Both country code and index provided. Only specify one")

        if country_code:
            query = f"SELECT * FROM countries WHERE country_code = '{country_code}'"
        else:
            query = f"""SELECT * FROM countries WHERE "index" = '{index}'"""

        return self.cursor.execute(query).fetchone()

    def get_row_count(self) -> int:
        query = "SELECT COUNT(*) FROM countries"
        return self.cursor.execute(query).fetchone()[0]

    def initialize_database(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.add_data_to_database()

    def add_data_to_database(self) -> None:
        countries_df = pd.read_csv(self.csv_path, keep_default_na=False)
        countries_df.to_sql("countries", self.conn, if_exists="replace")
