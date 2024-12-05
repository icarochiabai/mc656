import pandas as pd
import sqlite3
import os
from io import BytesIO
from scripts.blur_image import blur_image

class DatabaseHandler:
    def __init__(
        self,
        db_path: str = "countries.db",
        csv_path="static/countries.csv",
        flags_path = "static/images",
        blur_levels = list(range(5,101,5)) 
    ) -> None:
        self.db_path = db_path
        self.csv_path = csv_path
        self.flags_path = flags_path
        self.blur_levels = blur_levels
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
    
    def get_country_flag(self, country_code) -> BytesIO:
        query = f"SELECT image WHERE country_code = '{country_code.lower()} FROM flags'"
        image_binary = self.cursor.execute(query).fetchone()[0]
        return BytesIO(image_binary)

    def get_row_count(self) -> int:
        query = "SELECT COUNT(*) FROM countries"
        return self.cursor.execute(query).fetchone()[0]

    def initialize_database(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.add_data_to_database()
        self.add_flags_to_database(self.blur_levels)

    def add_data_to_database(self) -> None:
        countries_df = pd.read_csv(self.csv_path, keep_default_na=False)
        countries_df.to_sql("countries", self.conn, if_exists="replace")
    
    def add_flags_to_database(self, blur_levels: list) -> None:
        data = []
        
        # Looping through all the images and saving them into a list
        for filename in os.listdir(self.flags_path):
            _filename = filename.lower()

            # We only want files that follow the pattern 'xx.png'
            if not _filename.endswith(".png") or len(_filename) != 6:
                continue
            
            file_path = os.path.join(self.flags_path, filename)
            binary_data = self.read_image(file_path)
            country_code = os.path.splitext(filename)[0]
            flag_data = {"country_code": country_code, "no_blur": binary_data}
            
            blurred_images = blur_image(blur_levels=blur_levels, image=binary_data)

            for index, blur_level in enumerate(blur_levels):
                flag_data.update({f"blur_{blur_level}": blurred_images[index]})
            
            data.append(flag_data)

        flags_df = pd.DataFrame(data)
        flags_df.to_sql("flags", self.conn, if_exists="replace", index=False, dtype={"image": "BLOB"})

    
    @staticmethod
    def read_image(file_path) -> bytes:
        with open(file_path, "rb") as file:
            return file.read()
