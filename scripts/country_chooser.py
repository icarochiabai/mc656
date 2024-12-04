"""
This module aims to pseudorandomly choose a country among all provided countries.
It uses the native random.choice method with a seed to allow the program to be restarted
and continue in the same sequence.
It should always choose a different country every day. In the rare case(1/40,000 chance) of the RNG
choosing the same country two days in a row, the number will be shuffled again
"""

import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import hashlib
import os


class CountryChooser:
    def __init__(
        self, seed: int | str = None, timezone: str = "Etc/UTC"
    ) -> None:
        self.seed = self.init_seed(seed)
        self.timezone = ZoneInfo(str(timezone))
        self.today_country_id = None
        self.yesterday_country_id = None

    def init_seed(self, seed) -> str:
        """
        Creates a new seed from urandom module if no seed is provided
        """
        if seed is None:
            seed = int.from_bytes(os.urandom(8))

        print(f"Seed being used: {seed}")

        return seed

    def get_hashed_seed(self, time: datetime) -> str:
        """
        Hashes the seed with the current date to add variability and ensure unique daily results.
        """
        seed_string = f"{self.seed}{time.strftime("%d%m%Y")}".encode()
        return hashlib.sha256(seed_string).hexdigest()

    def choose(self, number_of_countries: int) -> int:
        """
        Chooses a country id pseudorandomly, ensuring it differs from the previous day's choice.
        """
        today_time = datetime.now(tz=self.timezone)
        yesterday_time = today_time - timedelta(hours=24)

        today_seed = self.get_hashed_seed(today_time)
        yesterday_seed = self.get_hashed_seed(yesterday_time)

        random.seed(yesterday_seed)
        self.yesterday_country_id = random.choice(range(number_of_countries-1))

        random.seed(today_seed)

        while True:
            candidate_id = random.choice(range(number_of_countries-1))
            if candidate_id != self.yesterday_country_id:
                self.today_country_id = candidate_id
                break

        return self.today_country_id
